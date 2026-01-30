import json
import unicodedata

def force_rebuild_dict(label_file, dict_file):
    chars = set()
    with open(label_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split('\t')
            if len(parts) < 2: continue
            try:
                # We normalize to NFC (Precomposed) to match standard OCR expectations
                data = json.loads(unicodedata.normalize('NFC', parts[1]))
                for item in data:
                    for char in item['transcription']:
                        if char != ' ': 
                            chars.add(char)
            except: continue

    # Write dictionary in NFC format
    with open(dict_file, 'w', encoding='utf-8') as f:
        for char in sorted(list(chars)):
            f.write(f"{char}\n")
    
    print(f"Dictionary Rebuilt! Total Unique Chars: {len(chars)}")

# Also normalize your label file to NFC to ensure a perfect match
def normalize_label_file(label_file):
    with open(label_file, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(label_file, 'w', encoding='utf-8') as f:
        f.write(unicodedata.normalize('NFC', content))
    print(f"Label file {label_file} normalized to NFC.")

force_rebuild_dict("vi_train_list.txt", "./data/vn_dictionary.txt")
normalize_label_file("vi_train_list.txt")