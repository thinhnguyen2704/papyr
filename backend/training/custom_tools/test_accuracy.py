from paddleocr import PaddleOCR
import os
import Levenshtein

# 1. Load the original Multilingual model
original_ocr = PaddleOCR(use_angle_cls=True, lang="vi")

# 2. Load your new Fine-tuned model
# Ensure the paths point to your exported inference model
custom_ocr = PaddleOCR(
    use_angle_cls=True,
    rec_model_dir="./output/rec_ppocr_v5_server_vi",
    rec_char_dict_path="./data/vn_dictionary.txt",
    lang="vi",
)


def test_comparison(image_path):
    print(f"\n--- Testing: {os.path.basename(image_path)} ---")

    # Run Original
    res_orig = original_ocr.ocr(image_path, cls=True)
    text_orig = (
        " ".join([line[1][0] for line in res_orig[0]]) if res_orig[0] else "No text"
    )

    # Run Custom
    res_custom = custom_ocr.ocr(image_path, cls=True)
    text_custom = (
        " ".join([line[1][0] for line in res_custom[0]]) if res_custom[0] else "No text"
    )

    print(f"ORIGINAL: {text_orig}")
    print(f"FINE-TUNED: {text_custom}")


def calculate_improvement(ground_truth, original_text, custom_text):
    score_orig = Levenshtein.ratio(ground_truth, original_text)
    score_custom = Levenshtein.ratio(ground_truth, custom_text)

    improvement = (score_custom - score_orig) * 100
    print(f"Accuracy Gain: {improvement:+.2f}%")


# Run on a folder of test images
test_folder = "./test_samples"
for img in os.listdir(test_folder):
    if img.endswith((".jpg", ".png", ".jpeg")):
        test_comparison(os.path.join(test_folder, img))
