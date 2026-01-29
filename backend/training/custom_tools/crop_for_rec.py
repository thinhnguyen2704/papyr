import cv2
import json
import os
import numpy as np
from tqdm import tqdm

def crop_for_recognition(label_file, output_dir, new_label_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    new_lines = []
    
    with open(label_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"Processing {len(lines)} full-page images...")
    for line_idx, line in enumerate(tqdm(lines)):
        try:
            img_path, json_str = line.strip().split('\t')
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            data = json.loads(json_str)
            for box_idx, item in enumerate(data):
                text = item['transcription']
                points = np.array(item['points'], dtype=np.float32)
                
                # Get the bounding box
                rect = cv2.boundingRect(points)
                x, y, w, h = rect
                
                # Add a small 2px margin if possible to avoid cutting characters
                y_min, y_max = max(0, y-2), min(img.shape[0], y+h+2)
                x_min, x_max = max(0, x-2), min(img.shape[1], x+w+2)
                
                crop = img[y_min:y_max, x_min:x_max]
                
                if crop.size == 0:
                    continue
                
                # Save crop
                crop_filename = f"crop_{line_idx}_{box_idx}.jpg"
                crop_full_path = os.path.join(output_dir, crop_filename)
                cv2.imwrite(crop_full_path, crop)
                
                # Standard Rec Format: relative_path \t text
                new_lines.append(f"{crop_full_path}\t{text}")
        except Exception as e:
            print(f"Error on line {line_idx}: {e}")

    with open(new_label_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f"Done! Created {len(new_lines)} crops and {new_label_file}")

if __name__ == "__main__":
    crop_for_recognition(
        label_file="vi_train_list.txt", 
        output_dir="./data/rec_crops", 
        new_label_file="vi_rec_train_list.txt"
    )