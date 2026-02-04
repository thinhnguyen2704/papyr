with open('./data/vn_dictionary.txt', 'r', encoding='utf-8') as f:
    valid_chars = set([line.strip() for line in f.readlines()])
valid_chars.add(' ') # Allow spaces

def clean_label_file(path):
    new_lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2: continue
            # Keep ONLY characters that exist in your dictionary
            clean_text = "".join([c for c in parts[1] if c in valid_chars])
            new_lines.append(f"{parts[0]}\t{clean_text}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

clean_label_file('vi_rec_train_list.txt')
clean_label_file('vi_rec_val_list.txt')
clean_label_file('vi_rec_test_list.txt')