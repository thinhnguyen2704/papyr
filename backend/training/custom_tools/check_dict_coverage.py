import json
import os

# Configuration - Update these paths if necessary
DICT_PATH = "data/vn_dictionary.txt"
LABEL_FILES = ["vi_rec_val_list.txt", "vi_rec_train_list.txt", "vi_rec_test_list.txt"] # Add all label files you use

def audit_dictionary():
    # 1. Load existing dictionary characters
    if not os.path.exists(DICT_PATH):
        print(f"Error: {DICT_PATH} not found.")
        return
        
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        # Using a set for O(1) lookups
        existing_chars = set(f.read().splitlines())
    
    print(f"Current dictionary size: {len(existing_chars)} characters.")

    # 2. Extract unique characters from all label files
    chars_in_labels = set()
    for label_file in LABEL_FILES:
        if not os.path.exists(label_file):
            print(f"Warning: {label_file} not found, skipping...")
            continue
            
        with open(label_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    # Split by tab to get the JSON part
                    parts = line.strip().split('\t')
                    if len(parts) < 2: continue
                    
                    annotations = json.loads(parts[1])
                    for ann in annotations:
                        text = ann.get('transcription', '')
                        for char in text:
                            # We ignore spaces as they aren't usually in the dict
                            if char != ' ':
                                chars_in_labels.add(char)
                except Exception as e:
                    continue

    # 3. Find missing characters
    missing_chars = sorted(list(chars_in_labels - existing_chars))

    if not missing_chars:
        print("✅ Success! No missing characters found.")
    else:
        print(f"⚠️ Found {len(missing_chars)} missing characters: {' '.join(missing_chars)}")
        
        # 4. Append missing characters to the dictionary
        with open(DICT_PATH, "a", encoding="utf-8") as f:
            for char in missing_chars:
                f.write(f"\n{char}")
        
        print(f"🚀 Added {len(missing_chars)} characters to {DICT_PATH}.")
        print("⚠️  REMINDER: You must delete your 'latest' checkpoint folder before restarting training!")

if __name__ == "__main__":
    audit_dictionary()