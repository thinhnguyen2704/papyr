import os
from PIL import Image

def scan_images(image_dir):
    print(f"--- Scanning directory: {image_dir} ---")
    if not os.path.exists(image_dir):
        print("Directory does not exist. Skipping.")
        return

    invalid_count = 0
    total_count = 0
    
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            total_count += 1
            file_path = os.path.join(image_dir, filename)
            
            # Check 1: File size
            if os.path.getsize(file_path) == 0:
                print(f"CORRUPTED (0 bytes): {filename}")
                invalid_count += 1
                continue
            
            # Check 2: Can PIL open it?
            try:
                with Image.open(file_path) as img:
                    img.verify() # Verify it's an image without loading pixels
            except Exception as e:
                print(f"INVALID IMAGE (cannot open): {filename} - {e}")
                invalid_count += 1

    print(f"Finished. Scanned: {total_count} | Found Invalid: {invalid_count}\n")

if __name__ == "__main__":
    # Update these paths to match your project
    base_data = "./data"
    folders = ["train_images", "val_images", "test_images"]
    
    for folder in folders:
        scan_images(os.path.join(base_data, folder))