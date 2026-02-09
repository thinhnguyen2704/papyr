import os

def verify_dataset(label_paths, data_dir="./"):
    print("🔍 Starting Dataset Validation...")
    for label_path in label_paths:
        missing_count = 0
        total_count = 0
        
        if not os.path.exists(label_path):
            print(f"❌ Label file not found: {label_path}")
            continue
            
        with open(label_path, "r", encoding="utf-8") as f:
            for line in f:
                total_count += 1
                parts = line.strip().split('\t') # PaddleOCR uses TAB
                
                if len(parts) < 2:
                    print(f"⚠️ Formatting Error in {label_path} at line {total_count}: No TAB separator found.")
                    continue
                
                img_path = parts[0]
                # Combine with data_dir if path is relative
                full_path = img_path if os.path.isabs(img_path) else os.path.join(data_dir, img_path)
                
                if not os.path.exists(full_path):
                    missing_count += 1
                    if missing_count <= 5: # Show only first 5 errors
                        print(f"❌ Missing Image: {full_path}")

        print(f"📊 Results for {label_path}:")
        print(f"   - Total entries: {total_count}")
        print(f"   - Missing images: {missing_count}")
        if missing_count == 0:
            print(f"   - ✅ Ready for training.")
        else:
            print(f"   - ❌ FIX REQUIRED: {missing_count} images were not found.")

# Update these to match your YAML exactly
verify_dataset(
    label_paths=["./vi_rec_train_list.txt", "./train_labels_huge.txt"],
    data_dir="./" 
)