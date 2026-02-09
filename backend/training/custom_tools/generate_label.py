import json
import os

# Root directory containing the 11 category folders
root_dir = './data/IMG_OCR_VIE_CN' 
output_label_file = 'train_labels.txt'

def generate_label():
    with open(output_label_file, 'w', encoding='utf-8') as out:
        # Loop through each of the 11 category folders
        for category in os.listdir(root_dir):
            category_path = os.path.join(root_dir, category)
            
            if os.path.isdir(category_path):
                print(f"Processing category: {category}")
                
                # Find all JSON files in the current category folder
                for file_name in os.listdir(category_path):
                    if file_name.endswith('.json'):
                        json_path = os.path.join(category_path, file_name)
                        
                        with open(json_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        image_name = data.get("imagePath", "unknown.jpg")
                        shapes = data.get("shapes", [])
                        
                        for i, shape in enumerate(shapes):
                            label = shape.get("label", "")
                            # Skip placeholders and empty labels
                            if label == "###" or not label.strip():
                                continue
                            
                            # Prefix with category name to ensure unique filenames
                            crop_name = f"{category}_crop_{i}_{image_name}"
                            out.write(f"train_crops/{crop_name}\t{label}\n")

generate_label()