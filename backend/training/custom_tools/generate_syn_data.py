import os
import cv2
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --- SETTINGS ---
TEXT_SOURCE = "./data/vn_corpus.txt"
OUTPUT_DIR = "./data/train_crops_huge"
LABEL_FILE = "./data/train_labels_huge.txt"
FONTS_DIR = "./data/fonts" # Matches your screenshot path
TOTAL_IMAGES = 100000 

if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

# --- MODIFIED FONT LOADER ---
fonts = []
for root, dirs, files in os.walk(FONTS_DIR):
    for file in files:
        if file.endswith(".ttf") or file.endswith(".otf"):
            fonts.append(os.path.join(root, file))

if not fonts:
    print(f"❌ Error: No font files found in {FONTS_DIR}. Check your path!")
    exit()
else:
    print(f"✅ Found {len(fonts)} fonts. Starting generation...")

# Load corpus
with open(TEXT_SOURCE, "r", encoding="utf-8") as f:
    corpus = [line.strip() for line in f.readlines() if len(line.strip()) > 5]

with open(LABEL_FILE, "w", encoding="utf-8") as f_label:
    for i in range(TOTAL_IMAGES):
        text = random.choice(corpus)
        if len(text) > 50: text = text[:50]
        
        font_path = random.choice(fonts)
        try:
            font_size = random.randint(22, 38)
            font = ImageFont.truetype(font_path, font_size)
            
            # Calculate text size
            bbox = font.getbbox(text)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            
            # Create canvas
            bg_color = (random.randint(220, 255), random.randint(220, 255), random.randint(220, 255))
            img = Image.new('RGB', (tw + 40, th + 40), color=bg_color)
            
            draw = ImageDraw.Draw(img)
            text_color = (random.randint(0, 60), random.randint(0, 60), random.randint(0, 60))
            draw.text((20, 15), text, font=font, fill=text_color)
            
            img_np = np.array(img)
            
            # Basic Augmentation
            if random.random() > 0.8:
                img_np = cv2.GaussianBlur(img_np, (3, 3), 0)
            
            # Save
            file_name = f"huge_{i}.jpg"
            save_path = os.path.join(OUTPUT_DIR, file_name)
            cv2.imwrite(save_path, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
            
            f_label.write(f"{save_path}\t{text}\n")
        except Exception as e:
            # Skip corrupted fonts or rendering errors
            continue
            
        if i % 5000 == 0: print(f"Progress: {i}/{TOTAL_IMAGES}")

print(f"🏁 Done! Dataset ready in {OUTPUT_DIR}")