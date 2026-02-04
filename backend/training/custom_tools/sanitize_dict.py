import os

def sanitize_dict(dict_path, label_path):
    # 1. Clean Dictionary
    with open(dict_path, 'r', encoding='utf-8') as f:
        # Strict strip and unique characters only
        chars = [line.strip() for line in f.readlines() if line.strip()]
    
    with open(dict_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(chars))
    
    char_set = set(chars)
    char_set.add(' ') # Add space to allowed characters if use_space_char is true

    # 2. Clean Label File
    clean_labels = []
    with open(label_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 2: continue
            img_path, text = parts[0], parts[1]
            
            # Remove any characters in the text that are NOT in the dictionary
            sanitized_text = "".join([c for c in text if c in char_set])
            clean_labels.append(f"{img_path}\t{sanitized_text}")

    with open(label_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(clean_labels))

sanitize_dict('./data/vn_dictionary.txt', './vi_rec_train_list.txt')
sanitize_dict('./data/vn_dictionary.txt', './vi_rec_val_list.txt')
sanitize_dict('./data/vn_dictionary.txt', './vi_rec_test_list.txt')
print("Synchronization Complete: Labels now only contain characters found in the dictionary.")