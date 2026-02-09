# 📜 Papyr OCR: Training & Development Report
## 1. Project Overview
Model: PP-OCRv5 (Server/Student)

Language: Vietnamese (Multilingual subset)

Objective: High-accuracy recognition for diverse document types (ID cards, newspapers, bills, book contents).

## 2. Training Run History
Run ID,Date,Config Changes,Dataset,Results (Acc / Edit Dis),Status
R1_BASE,2026-02-05,"Width=320, BS=128",Real (11 cats),0.0% / 0.05,Failed (Alphabet Soup)
R2_WIDE,2026-02-07,"Width=640, BS=64",Real (11 cats),2.6% / 0.33,Underfit (Peaked at E85)
R3_HUGE,2026-02-09,"Width=640, BS=48",10k Real + 100k Synth,Queueing...,Preparing Data

## 3. Incident & Solution Log
Detailed records of technical "blockers" met during the project.

### Incident #001: Character Crushing (The "Alphabet Soup" Error)
Issue: Predictions returned repetitive, nonsensical characters (e.g., Ỏ Ỏ Ỏ 1 1).

Cause: The default 320px width was too small for Vietnamese long-text lines. Characters were being compressed into the same feature space.

Solution: Increased image_shape width to 640px and max_text_length to 64.

### Incident #002: Kernel Crash (Exit Code -1073740791)
Issue: Python crashed immediately upon starting training.

Cause: Windows multiprocessing conflict with num_workers > 0 and extreme VRAM usage (23.8GB/24GB) on the RTX 4090.

Solution: Set num_workers: 0 in the YAML and reduced batch_size_per_card to 48.

### Incident #003: Key Error 'LinearWarmup_LR'
Issue: KeyError: 'LinearWarmup_LR' when resuming from a checkpoint.

Cause: Resuming a model trained without a warmup into a config with a 5-epoch warmup. The optimizer state didn't match.

Solution: Switched to Global.pretrained_model to load only weights, ignoring the broken optimizer state.

## 4. Hyperparameter Evolution
Parameter,Run 1,Run 2,Run 3 (Next)
Batch Size,128,64,48 (Safety)
Learning Rate,0.001,0.0005,0.0002
Image Shape,"[48, 320]","[48, 640]","[48, 640]"
Warmup Epochs,0,5,2

## 5. Performance Analysis (R2_WIDE)
Analysis of the 500-epoch run completed on 2026-02-07.

Observation: The model reached its best accuracy (2.6%) very early (Epoch 85) and then plateaued.

The "Gap": There is a massive gap between Accuracy (2.6%) and Edit Distance (33%).

Interpretation: The model is recognizing about 1/3 of the characters correctly, but almost zero full sentences. This confirms the model lacks "linguistic context" (it doesn't know common Vietnamese word patterns).

Conclusion: Real-world data is too sparse for the complexity of the 11 categories.

## 6. Current Strategy (Phase 3: The Data Factory)
Action: Generate 100,000 synthetic images using a text corpus scraped from VnExpress.

Goal: Teach the model the "logic" of Vietnamese syllables (e.g., that Qu is often followed by y or a).

Success Metric: Target an Edit Distance > 0.75 and Accuracy > 30% for the next run.


### 📑 Journal Entry: 
Checkpoint Verification
Folder Audit: Confirmed ./output/papyr_rec/ is receiving updates. Model Health: latest.pdparams is updating every 1000 steps. Validation: Even if accuracy is currently lower than the "best" checkpoint, the training is mathematically progressing as evidenced by the stable Loss.

R3_HUGE Phase 2
Resume Status: Successfully hot-swapped YAML config. New Baseline: Training speed increased by ~15% (20.7 IPS). ETA reduced to 11 days. Validation Config: Evaluation now scheduled every 1000 steps (~45-50 mins). Current Goal: Maintain stability and monitor for the first "Best Model" overwrite after the warmup period.

Reliability Check
Power Configuration: Verified "Plugged in" sleep mode is disabled. Storage Verification: Monitored ./output/papyr_rec/ for file integrity. Checkpoint Strategy: Confirmed that latest.pdparams is the primary recovery point, while best_accuracy.pdparams serves as the final production candidate.