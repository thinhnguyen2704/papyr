import cv2
import os

# --- Configuration ---
IMAGE_FOLDER = './data/test_images'  # Path where im0001.jpg etc. are stored
LABEL_FOLDER = './data/labels'  # Path where gt_1.txt etc. are stored
OUTPUT_FOLDER = './data/test_crops'  # Where the cropped images will go
OUTPUT_LABEL = './vi_rec_test_list.txt' # The final list for PaddleOCR

# Create output folder
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

crop_count = 0
train_list = []

# Loop through your images
for i in range(1801, 2000):
    img_name = f"im{i:04d}.jpg"
    label_name = f"gt_{i}.txt"
    
    img_path = os.path.join(IMAGE_FOLDER, img_name)
    label_path = os.path.join(LABEL_FOLDER, label_name)
    
    if not os.path.exists(img_path) or not os.path.exists(label_path):
        continue

    # Load image
    image = cv2.imread(img_path)
    if image is None:
        continue

    # Read label file
    with open(label_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_idx, line in enumerate(lines):
        # Expected format: x1,y1,x2,y2,x3,y3,x4,y4,text
        parts = line.strip().split(',')
        if len(parts) < 9 or parts[8] == "###": # Skip "don't care" labels
            continue
        
        try:
            # Extract coordinates
            coords = [int(p) for p in parts[:8]]
            text = ",".join(parts[8:]) # Handle text that might contain commas
            
            # Get bounding box for cropping
            x_coords = coords[0::2]
            y_coords = coords[1::2]
            xmin, xmax = min(x_coords), max(x_coords)
            ymin, ymax = min(y_coords), max(y_coords)
            
            # Crop the image
            crop = image[ymin:ymax, xmin:xmax]
            
            if crop.size == 0:
                continue

            # Save the crop
            crop_filename = f"crop_{i:04d}_{line_idx}.jpg"
            crop_save_path = os.path.join(OUTPUT_FOLDER, crop_filename)
            cv2.imwrite(crop_save_path, crop)
            
            # Add to the PaddleOCR training list format: path\tlabel
            train_list.append(f"{OUTPUT_FOLDER}/{crop_filename}\t{text}")
            crop_count += 1
            
        except Exception as e:
            print(f"Error processing {img_name} at line {line_idx}: {e}")

# Save the final training list
with open(OUTPUT_LABEL, 'w', encoding='utf-8') as f:
    f.write("\n".join(train_list))

print(f"✅ Successfully created {crop_count} crops and updated {OUTPUT_LABEL}")