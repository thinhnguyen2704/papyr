import os

# Define your paths - Use absolute paths for reliability
dict_path = r"C:\Users\thinh.nguyen\Documents\PersonalProject\papyr\backend\training\data\vn_dictionary.txt"
label_path = r"C:\Users\thinh.nguyen\Documents\PersonalProject\papyr\backend\training\vi_rec_train_list.txt"

# 1. Check Dictionary
if not os.path.exists(dict_path):
    print(f"❌ DICTIONARY NOT FOUND: {dict_path}")
else:
    with open(dict_path, 'r', encoding='utf-8') as f:
        vocab = {line.strip('\n').strip('\r') for line in f}
    print(f"✅ Dictionary loaded: {len(vocab)} characters.")

# 2. Check Labels and Image Paths
if not os.path.exists(label_path):
    print(f"❌ LABEL FILE NOT FOUND: {label_path}")
else:
    missing_images = 0
    missing_chars = set()
    total_lines = 0
    
    with open(label_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            total_lines += 1
            parts = line.strip().split('\t')
            if len(parts) != 2:
                print(f"⚠️ Line {i+1} has wrong format (split by tab failed).")
                continue
            
            img_path, text = parts
            # Check if image exists
            if not os.path.exists(img_path):
                missing_images += 1
                if missing_images <= 5:
                    print(f"❌ Image missing: {img_path}")
            
            # Check for characters not in dictionary
            for char in text:
                if char not in vocab and char != ' ':
                    missing_chars.add(char)

    print(f"\n--- Results for {total_lines} lines ---")
    if missing_images == 0:
        print("✅ All image paths are valid.")
    else:
        print(f"❌ Total missing images: {missing_images}")
        
    if not missing_chars:
        print("✅ All characters exist in dictionary.")
    else:
        print(f"❌ Missing characters in dictionary: {' '.join(list(missing_chars))}")