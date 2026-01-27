from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from paddleocr import PaddleOCR
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

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
ocr_engines = {
    "en": PaddleOCR(
        use_angle_cls=True,
        lang="en",
    ),
    "vi": PaddleOCR(
        use_angle_cls=True,
        lang="vi",
        det_db_unclip_ratio=2.5,  # Helps capture full Vietnamese diacritics
        det_db_box_thresh=0.6,  # Filters out smaller noise dots
        rec_image_shape="3, 48, 320",  # Standard for high-res recognition
    ),
}


def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Increase contrast and sharpen
    # Adaptive Thresholding helps handle uneven lighting/shadows
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    # Just a slight blur to remove digital noise
    processed = cv2.GaussianBlur(gray, (3, 3), 0)
    return processed


@app.post("/scan")
async def scan_image(lang: str, file: UploadFile = File(...)):
    print(f"Received scan request for language: {lang}")
    # Read image from upload
    data = await file.read()
    nparr = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Clean the image before OCR
    cleaned_img = preprocess_image(image)
    ocr = ocr_engines.get(lang, ocr_engines["vi"])

    # Perform OCR
    result = ocr.ocr(cleaned_img, cls=True)
    extracted_text = []
    # 1. Check if the OCR engine returned None or an empty list
    if result is None or not result or result[0] is None:
        raise HTTPException(
            status_code=422,
            detail="no_text_found",
        )
    
    try:
        extracted_text = ""
        for line in result[0]:
            # result[0] format is usually [[ [coords], (text, score) ], ...]
            text = line[1][0]
            extracted_text += text + " "

        return {"text": extracted_text.strip()}

    except (TypeError, IndexError):
        raise HTTPException(status_code=422, detail="no_text_found")
    finally:
        print("OCR Result:", extracted_text)
        return {"data": extracted_text}


if __name__ == "__main__":
    import uvicorn

    print("🚀 Papyr Engine Starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
