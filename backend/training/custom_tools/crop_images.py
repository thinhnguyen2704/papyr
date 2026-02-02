import os
import cv2
import json
import numpy as np
from tqdm import tqdm

# Configuration
LABEL_FILE = "vi_test_list.txt" # Input label file with full images and annotations
OUTPUT_DIR = "data/rec_test_crops" # Directory to save cropped images
NEW_LIST = "vi_rec_test_list.txt" # Output label file for recognition model

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_rotate_crop_image(img, points):
    # Standard PaddleOCR cropping logic for 4-point polygons
    img_crop_width = int(max(np.linalg.norm(points[0] - points[1]), np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(max(np.linalg.norm(points[0] - points[3]), np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0], [img_crop_width, 0], [img_crop_width, img_crop_height], [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(img, M, (img_crop_width, img_crop_height), borderMode=cv2.BORDER_REPLICATE)
    return dst_img

with open(LABEL_FILE, "r", encoding="utf-8") as f, \
     open(NEW_LIST, "w", encoding="utf-8") as f_out:
    
    lines = f.readlines()
    for i, line in enumerate(tqdm(lines, desc="Cropping Images")):
        parts = line.strip().split('\t')
        if len(parts) < 2: continue
        
        img_path = parts[0]
        annotations = json.loads(parts[1])
        
        # Load the full source image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Skip: {img_path} not found.")
            continue

        for j, ann in enumerate(annotations):
            text = ann['transcription']
            points = np.array(ann['points'], dtype=np.float32)
            
            # Perform the crop
            dst_img = get_rotate_crop_image(img, points)
            
            # Save the cropped word image
            crop_name = f"crop_{i}_{j}.jpg"
            save_path = os.path.join(OUTPUT_DIR, crop_name)
            cv2.imwrite(save_path, dst_img)
            
            # Write the new V5 format line for the recognition model
            # Format: path/to/crop.jpg \t {"transcription": "TEXT"}
            out_label = {"transcription": text}
            f_out.write(f"{OUTPUT_DIR}/{crop_name}\t{json.dumps(out_label, ensure_ascii=False)}\n")

print(f"Finished! New labels saved to {NEW_LIST}")