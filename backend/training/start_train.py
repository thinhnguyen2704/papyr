import os
import paddle
import sys

def run_training():
    # 1. Health check for GPU/CPU
    print("--- Environment Check ---")
    paddle.utils.run_check()
    
    # 2. Verify Config exists
    config_path = "vi_PP-OCRv5_server_rec.yml"
    if not os.path.exists(config_path):
        print(f"Error: Config file {config_path} not found!")
        return

    print(f"--- Starting Fine-tuning with {config_path} ---")
    
    # Senior Tip: Point to the actual PaddleOCR tool. 
    # If your script is in the 'training' root, the command is:
    command = f"python tools/train.py -c {config_path}"
    
    exit_code = os.system(command)
    
    if exit_code == 0:
        print("Training completed successfully. Check the ./output/ folder.")
    else:
        print(f"Training failed with exit code: {exit_code}")

if __name__ == "__main__":
    run_training()