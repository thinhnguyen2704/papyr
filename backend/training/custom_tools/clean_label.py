input_files = ['vi_rec_train_list.txt', 'vi_rec_val_list.txt', 'vi_rec_test_list.txt']

for file_path in input_files:
    clean_lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Tìm vị trí của file ảnh (thường kết thúc bằng .jpg hoặc .png)
            if '.jpg' in line:
                parts = line.split('.jpg', 1)
                img_path = parts[0] + '.jpg'
                label = parts[1].strip()
                clean_lines.append(f"{img_path.strip()}\t{label}\n")
            elif '.png' in line:
                parts = line.split('.png', 1)
                img_path = parts[0] + '.png'
                label = parts[1].strip()
                clean_lines.append(f"{img_path.strip()}\t{label}\n")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)

print("✅ Đã sửa xong định dạng Tab cho các file nhãn.")