import random
import os

def split_dataset(label_file, output_dir, train_ratio=0.8, val_ratio=0.1):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read all lines from the master label file
    with open(label_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Shuffle the dataset to mix categories (ID cards, Bills, etc.)
    random.seed(42)  # For reproducibility
    random.shuffle(lines)

    total_count = len(lines)
    train_end = int(total_count * train_ratio)
    val_end = train_end + int(total_count * val_ratio)

    # Split the lines
    train_lines = lines[:train_end]
    val_lines = lines[train_end:val_end]
    test_lines = lines[val_end:]

    # Write the split files
    splits = {
        'vi_rec_train_list.txt': train_lines,
        'vi_rec_val_list.txt': val_lines,
        'vi_rec_test_list.txt': test_lines
    }

    for file_name, data in splits.items():
        save_path = os.path.join(output_dir, file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.writelines(data)
        print(f"Saved {len(data)} lines to {save_path}")

# Usage
# This will use the master labels generated from your 11 folders
split_dataset('vi_rec_train_list.txt', './')