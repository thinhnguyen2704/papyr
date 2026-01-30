import os
import cv2
from tqdm import tqdm

def resize_giant_images(image_dir, max_size=2000):
    print(f"Scanning {image_dir} for images larger than {max_size}px...")
    
    # Supported formats
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
    files = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_exts)]
    
    count = 0
    for filename in tqdm(files):
        img_path = os.path.join(image_dir, filename)
        
        # We use imread sparingly to save memory during the scan
        # For very large files, this might still be heavy
        try:
            # Get dimensions without fully loading if possible, 
            # but cv2.imread is most reliable for this workflow
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            h, w = img.shape[:2]
            
            if h > max_size or w > max_size:
                # Calculate new dimensions
                if w > h:
                    new_w = max_size
                    new_h = int(h * (max_size / w))
                else:
                    new_h = max_size
                    new_w = int(w * (max_size / h))
                
                resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                cv2.imwrite(img_path, resized_img)
                count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Update this path to your actual image directory
    train_dir = r"C:\Users\thinh.nguyen\Documents\PersonalProject\papyr\backend\training\data\train_images"
    resize_giant_images(train_dir)