import re
from datetime import datetime

def generate_report(log_path):
    print(f"--- R3_HUGE Training Report Card ({datetime.now().strftime('%Y-%m-%d')}) ---")
    print(f"{'Step':<10} | {'Loss':<10} | {'Acc':<10} | {'Edit Dist':<12} | {'LR':<10}")
    print("-" * 60)

    pattern = re.compile(r"global_step: (\d+), lr: ([\d.]+), acc: ([\d.]+), norm_edit_dis: ([\d.]+), loss: ([\d.]+)")
    
    last_step = -1
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                step = int(match.group(1))
                # Print stats every 10,000 steps
                if step % 10000 == 0 and step != last_step:
                    lr = match.group(2)
                    acc = float(match.group(3))
                    ed = float(match.group(4))
                    loss = match.group(5)
                    print(f"{step:<10} | {loss:<10} | {acc:<10.4f} | {ed:<12.4f} | {lr:<10}")
                    last_step = step

if __name__ == "__main__":
    generate_report("./output/papyr_rec/train.log")