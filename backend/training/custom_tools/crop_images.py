import cv2
import json
import os
import numpy as np

def crop_text_regions(label_file, output_dir, output_label_file):
    # if not os.path.exists(output_dir): 
    #     os.makedirs(output_dir)
    
    new_labels = []
    
    with open(label_file, 'r', encoding='utf-8') as f:
        for line_idx, line in enumerate(f):
            img_path, json_str = line.strip().split('\t')
            img = cv2.imread(img_path)
            if img is None: continue
            
            data = json.loads(json_str)
            for box_idx, item in enumerate(data):
                pts = np.array(item['points'], dtype=np.float32)
                # Crop logic (Perspective transform or simple bounding box)
                rect = cv2.boundingRect(pts)
                x, y, w, h = rect
                crop = img[y:y+h, x:x+w]
                
                if crop.size == 0: continue
                
                crop_name = f"line_{line_idx}_{box_idx}.jpg"
                crop_path = os.path.join(output_dir, crop_name)
                cv2.imwrite(crop_path, crop)
                
                # Write the simple format Recognition models need:
                # path/to/image [TAB] text
                new_labels.append(f"{crop_path}\t{item['transcription']}")
                
    with open(output_label_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_labels))

crop_text_regions("vi_train_list.txt", "./data/rec_crops", "vi_rec_train_list.txt")