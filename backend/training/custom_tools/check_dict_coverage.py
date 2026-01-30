import unicodedata
import json

def check_dictionary_coverage(label_file, dict_file):
    # Load dictionary into a set
    with open(dict_file, 'r', encoding='utf-8') as f:
        dictionary = {line.strip() for line in f}
    
    missing_chars = set()
    with open(label_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Assuming format: path\ttext or path\t[{"transcription": "text",...}]
            parts = line.split('\t')
            if len(parts) < 2: continue
            text = parts[1]
            
            # Check every character in the text
            for char in text:
                if char not in dictionary and char not in [' ', '\t', '\n', '\r']:
                    missing_chars.add(char)
    
    if missing_chars:
        print(f"Found {len(missing_chars)} missing characters!")
        print(f"Add these to your dictionary: {''.join(sorted(missing_chars))}")
    else:
        print("All characters in labels are covered by the dictionary.")



def normalize_and_check(label_path, dict_path):
    # Load and normalize dictionary
    with open(dict_path, 'r', encoding='utf-8') as f:
        dictionary = {unicodedata.normalize('NFC', line.strip()) for line in f}
    
    missing = set()
    with open(label_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Normalize the whole line to NFC
            line = unicodedata.normalize('NFC', line)
            # Find characters not in dictionary
            # Standard PaddleOCR index usually starts from 0 or 1, 
            # but the encoder needs the raw char in the dict file.
            for char in line.split('\t')[-1]: # Check the JSON part
                if char not in dictionary and char not in [' ', '"', ':', '{', '}', '[', ']', ',', '.', '\t', '\n', '\\']:
                    missing.add(char)

    if missing:
        print(f"STILL MISSING characters: {''.join(sorted(missing))}")
    else:
        print("Normalization check passed. Dictionary is complete.")


def strict_check(label_file, dict_file):
    with open(dict_file, 'r', encoding='utf-8') as f:
        # PaddleOCR dict usually has 1 char per line
        d = {line.strip('\n').strip('\r') for line in f}
    
    with open(label_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            parts = line.split('\t')
            if len(parts) < 2: continue
            labels = json.loads(parts[1])
            for item in labels:
                text = item['transcription']
                for char in text:
                    # Ignore standard symbols handled by the system
                    if char not in d and char not in [' ']:
                        print(f"ERROR: Line {i+1} has missing char: [{char}] (Hex: {hex(ord(char))})")
                        print(f"Full text: {text}")
                        return # Stop at first error


if __name__ == "__main__":
    check_dictionary_coverage("./vi_rec_train_list.txt", "./data/vn_dictionary.txt")
    normalize_and_check("vi_rec_train_list.txt", "./data/vn_dictionary.txt")
    strict_check("vi_rec_train_list.txt", "./data/vn_dictionary.txt")