import os
import shutil
import subprocess

def archive(step_name):
    # 1. Create the milestone directory
    target_dir = f"milestones/{step_name}"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    # 2. Archive the predictions (ensure path matches your config)
    # PaddleOCR usually saves to output/rec/predicts_rec.txt by default
    source_predicts = "./output/rec/predicts_rec.txt" 
    if os.path.exists(source_predicts):
        shutil.copy(source_predicts, f"{target_dir}/predicts_rec.txt")
        print(f"Copied predictions to {target_dir}")
    else:
        print("Error: predicts_rec.txt not found. Run inference first.")

    # 3. Generate and save the Report Card summary
    report_file = f"milestones/report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        # Call your existing report_card script and pipe output to file
        subprocess.run(["python", "custom_tools/report_card.py"], stdout=f)
    
    print(f"Report Card archived to {report_file}")
    print(f"--- Milestone {step_name} Locked ---")

if __name__ == "__main__":
    # You can change this string whenever you hit a new big step
    archive("step_116k")