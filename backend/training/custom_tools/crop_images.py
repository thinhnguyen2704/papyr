import json
import cv2
import numpy as np
import os

root_dir = './data/IMG_OCR_VIE_CN'
output_dir = 'train_crops'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def crop_images():
    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        
        if os.path.isdir(category_path):
            for file_name in os.listdir(category_path):
                if file_name.endswith('.json'):
                    json_path = os.path.join(category_path, file_name)
                    
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Assume .jpg is in the same folder as the .json
                    image_filename = data.get("imagePath", "")
                    image_path = os.path.join(category_path, image_filename)
                    
                    img = cv2.imread(image_path)
                    if img is None:
                        continue

                    for i, shape in enumerate(data.get("shapes", [])):
                        label = shape.get("label", "")
                        if label == "###" or not label.strip():
                            continue
                            
                        # Handle polygon points
                        points = np.array(shape.get("points", []), dtype=np.int32)
                        x, y, w, h = cv2.boundingRect(points)
                        
                        # Add a small 2-pixel padding to avoid cutting off diacritics
                        crop = img[max(0, y-2):y+h+2, max(0, x-2):x+w+2]
                        
                        crop_filename = f"{category}_crop_{i}_{image_filename}"
                        cv2.imwrite(os.path.join(output_dir, crop_filename), crop)

crop_images()