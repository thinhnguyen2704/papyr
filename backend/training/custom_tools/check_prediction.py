import os
import sys
# Thêm đường dẫn tới thư mục gốc của PaddleOCR nếu cần
sys.path.append('.')

from paddleocr import PaddleOCR
import random

# 1. Cấu hình đường dẫn
# Sử dụng checkpoint epoch 5 bạn vừa đạt được
model_dir = './output/papyr_rec/best_model'
dict_path = './data/vn_dictionary.txt'
val_list = './vi_rec_val_list.txt'

# 2. Khởi tạo OCR
# Lưu ý: dùng đúng cấu hình rec_image_shape bạn đã chỉnh trong YAML
ocr = PaddleOCR(rec_model_dir=model_dir, 
                rec_char_dict_path=dict_path,
                use_angle_cls=False,
                lang='vi',
                rec_image_shape="3, 48, 480") # Đảm bảo khớp với YAML

# 3. Lấy ngẫu nhiên 5 ảnh từ tập Validation để soi
with open(val_list, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    samples = random.sample(lines, 5)

print(f"\n{'GROUND TRUTH':<30} | {'PREDICTION':<30} | {'CONFIDENCE'}")
print("-" * 80)

for line in samples:
    img_path, gt_text = line.strip().split('\t')
    
    # Dự đoán
    result = ocr.ocr(img_path, det=False, cls=False)
    
    if result and result[0]:
        pred_text, score = result[0][0]
    else:
        pred_text, score = "NONE", 0.0
        
    print(f"{gt_text[:30]:<30} | {pred_text[:30]:<30} | {score:.4f}")