from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from paddleocr import PaddleOCR
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize PaddleOCR (This can be swapped with your fine-tuned model path)
# Use 'use_gpu=False' if you don't have an NVIDIA GPU
ocr = PaddleOCR(use_angle_cls=True, lang="latin")


def preprocess_image(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Increase contrast and sharpen
    # Adaptive Thresholding helps handle uneven lighting/shadows
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return processed


engines = {}


def get_ocr_engine(lang: str):
    if lang not in engines:
        print(f"--- Loading {lang} model for the first time ---")
        engines[lang] = PaddleOCR(
            use_angle_cls=True,
            lang=lang,
            det_db_unclip_ratio=2.5,  # Helps capture full Vietnamese diacritics
            det_db_box_thresh=0.5,  # Filters out smaller noise dots
            rec_image_shape="3, 48, 320",  # Standard for high-res recognition
        )
    return engines[lang]


@app.post("/scan")
async def scan_image(file: UploadFile = File(...), lang: str = "en"):
    # Read image from upload
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Clean the image before OCR
    cleaned_img = preprocess_image(image)
    ocr = get_ocr_engine(lang)
    # Pre-processing for Book Curves
    # Convert to grayscale and apply adaptive thresholding
    gray = cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2GRAY)
    cleaned_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Perform OCR
    result = ocr.ocr(cleaned_img, cls=True)

    # Format the output for the React frontend
    extracted_text = []
    for line in result[0]:
        extracted_text.append(line[1][0])

    print("OCR Result:", extracted_text)
    return {"data": extracted_text}


if __name__ == "__main__":
    import uvicorn

    print("🚀 Papyr Engine Starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
