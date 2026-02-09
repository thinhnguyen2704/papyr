import collections

# Path to your PaddleOCR training list
label_file = 'vi_rec_train_list.txt'

def analyze_char_frequency(file_path):
    char_counts = collections.Counter()
    total_lines = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    label = parts[1]
                    char_counts.update(label)
                    total_lines += 1
        
        # Sort by frequency (ascending to see what needs more data)
        sorted_counts = sorted(char_counts.items(), key=lambda x: x[1])
        
        print(f"Total images processed: {total_lines}")
        print(f"Unique characters found: {len(sorted_counts)}")
        print("\n--- Character Frequency (Lowest to Highest) ---")
        print(f"{'Char':<10} | {'Count':<10}")
        print("-" * 25)
        
        for char, count in sorted_counts:
            # Handle space visualization
            display_char = f"'{char}'" if char != " " else "'space'"
            print(f"{display_char:<10} | {count:<10}")
            
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")

if __name__ == "__main__":
    analyze_char_frequency(label_file)