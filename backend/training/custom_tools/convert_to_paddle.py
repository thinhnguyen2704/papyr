import os
import json

def convert_folder_to_paddle(labels_dir, images_dir, output_file):
    """
    Converts a specific pair of (labels_folder, images_folder) 
    into a single PaddleOCR list file.
    """
    if not os.path.exists(labels_dir):
        print(f"Skipping: Labels directory not found at {labels_dir}")
        return

    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    print(f"Processing {images_dir}... Found {len(label_files)} labels.")

    count = 0
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for label_file in label_files:
            try:
                # Extract index from 'gt_123.txt'
                num_part = ''.join(filter(str.isdigit, label_file))
                # Map to 'im0123.jpg' (or whatever your naming convention is)
                img_name = f"im{int(num_part):04d}.jpg"
                img_path = os.path.abspath(os.path.join(images_dir, img_name))
            except Exception:
                continue
                
            label_path = os.path.join(labels_dir, label_file)
            image_annotations = []

            if not os.path.exists(img_path):
                # Optional: print(f"Warning: Image {img_path} missing")
                continue

            with open(label_path, 'r', encoding='utf-8-sig') as f_in:
                for line in f_in:
                    parts = line.strip().split(',', 8)
                    if len(parts) < 9 or parts[8] == '###':
                        continue
                    
                    coords = [float(x) for x in parts[:8]]
                    points = [[coords[0], coords[1]], [coords[2], coords[3]], 
                              [coords[4], coords[5]], [coords[6], coords[7]]]
                    
                    image_annotations.append({"transcription": parts[8], "points": points})
            
            if image_annotations:
                f_out.write(f"{img_path}\t{json.dumps(image_annotations, ensure_ascii=False)}\n")
                count += 1
    print(f"Done! Created {output_file} with {count} samples.")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_ROOT = os.path.join(SCRIPT_DIR, '..', 'data')
    
    # Define your folder pairs
    # (Label Folder Name, Image Folder Name, Output Filename)
    tasks = [
        ('labels', 'train_images', 'vi_train_list.txt'),
        ('labels', 'val_images', 'vi_val_list.txt'),
        ('labels', 'test_images', 'vi_test_list.txt')
    ]

    for lab_f, img_f, out_f in tasks:
        convert_folder_to_paddle(
            labels_dir=os.path.join(DATA_ROOT, lab_f),
            images_dir=os.path.join(DATA_ROOT, img_f),
            output_file=os.path.join(SCRIPT_DIR, '..', out_f)
        )