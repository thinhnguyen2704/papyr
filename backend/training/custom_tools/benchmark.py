import os
import csv
import time
import Levenshtein
from paddleocr import PaddleOCR

# --- CONFIGURATION ---
# Format: filename|ground_truth_text
GROUND_TRUTH_PATH = "test_samples/ground_truth.txt"
IMAGE_DIR = "test_samples/"
OUTPUT_CSV = "ocr_benchmark_report.csv"

# Initialize Models
print("Loading models...")
stock_ocr = PaddleOCR(use_angle_cls=True, lang="vi")
tuned_ocr = PaddleOCR(
    use_angle_cls=True,
    rec_model_dir="./inference/vi_model_v4",
    rec_char_dict_path="./vi_dict.txt",
    lang="vi",
)


def get_text(result):
    if not result or result[0] is None:
        return ""
    return " ".join([line[1][0] for line in result[0]]).strip()


def run_benchmark():
    results = []

    # Load ground truth into a dict
    gt_data = {}
    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                gt_data[parts[0]] = parts[1]

    print(f"Starting benchmark on {len(gt_data)} images...")

    for img_name, gt_text in gt_data.items():
        img_path = os.path.join(IMAGE_DIR, img_name)
        if not os.path.exists(img_path):
            continue

        # Benchmark Stock
        start = time.time()
        res_stock = get_text(stock_ocr.ocr(img_path))
        time_stock = time.time() - start

        # Benchmark Tuned
        start = time.time()
        res_tuned = get_text(tuned_ocr.ocr(img_path))
        time_tuned = time.time() - start

        # Calculate Accuracy (0.0 to 1.0)
        acc_stock = Levenshtein.ratio(gt_text, res_stock)
        acc_tuned = Levenshtein.ratio(gt_text, res_tuned)

        results.append(
            {
                "filename": img_name,
                "ground_truth": gt_text,
                "stock_text": res_stock,
                "tuned_text": res_tuned,
                "stock_acc": round(acc_stock * 100, 2),
                "tuned_acc": round(acc_tuned * 100, 2),
                "improvement": round((acc_tuned - acc_stock) * 100, 2),
                "speed_diff_ms": round((time_tuned - time_stock) * 1000, 2),
            }
        )

    # Write to CSV
    keys = results[0].keys()
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(f"✅ Benchmark complete! Report saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    run_benchmark()
