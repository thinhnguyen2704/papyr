import os
# Note: In production, we typically use PaddleOCR's CLI tools to train, 
# but this script prepares the environment.
def run_training():
    print("Starting Fine-tuning...")
    # Senior Tip: Use the config file to point to your /data folder
    command = "python3 tools/train.py -c configs/rec/PP-OCRv3/en_PP-OCRv3_rec.yml"
    os.system(command)

if __name__ == "__main__":
    run_training()