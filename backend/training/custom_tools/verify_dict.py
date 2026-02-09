def verify_dictionary(label_file, dict_file):
    # Đọc từ điển hiện tại
    with open(dict_file, 'r', encoding='utf-8') as f:
        dictionary = set([line.strip() for line in f.readlines()])
    
    # PaddleOCR tự động xử lý khoảng trắng nếu use_space_char: True
    dictionary.add(' ') 
    
    missing_chars = set()
    total_chars = set()

    # Đọc tất cả nhãn từ file master vừa tạo
    with open(label_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                label = parts[1]
                for char in label:
                    total_chars.add(char)
                    if char not in dictionary:
                        missing_chars.add(char)

    print(f"Tổng số ký tự duy nhất trong nhãn: {len(total_chars)}")
    if not missing_chars:
        print("✅ Tuyệt vời! Từ điển của bạn đã bao phủ 100% ký tự trong tập dữ liệu mới.")
    else:
        print(f"❌ Cảnh báo! Phát hiện {len(missing_chars)} ký tự thiếu trong từ điển:")
        print(list(missing_chars))
        print("\nBạn nên thêm các ký tự này vào 'vn_dictionary.txt' để tránh lỗi Acc = 0.")

# Sử dụng
verify_dictionary('./vi_rec_test_list.txt', './data/vn_dictionary.txt')