from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
import json
import time

from app.endpoints.metrics import track_latency

router = APIRouter()

# Paths to metadata and weights
MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "weights"
METADATA_FILE = Path(__file__).resolve().parent.parent.parent / "model_metadata.json"
DEFAULT_MODEL_FILE = Path(__file__).resolve().parent.parent.parent / "default_model.txt"

# Load metadata from JSON
def load_metadata():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Load default model key from text file
def get_default_model_key():
    if DEFAULT_MODEL_FILE.exists():
        with open(DEFAULT_MODEL_FILE, "r") as f:
            return f.read().strip()
    return "best_model_v6"  # fallback if file doesn't exist

# Load model from metadata and weights directory
def load_model(model_key: str):
    metadata = load_metadata()
    if model_key not in metadata:
        raise HTTPException(status_code=404, detail=f"Model '{model_key}' not found in metadata.")
    
    model_filename = metadata[model_key]["model"]
    model_path = MODEL_DIR / model_filename

    print(f"[DEBUG] Trying to load model at: {model_path}")
    
    if not model_path.exists():
        raise HTTPException(status_code=404, detail=f"Model file '{model_filename}' not found in weights directory.")
    
    return YOLO(str(model_path)), model_key

# Prediction endpoint
@router.post("/predict")
async def predict_batch(
    images: List[UploadFile] = File(...),
    model: Optional[str] = Form(None)
):
    model_key = model.strip() if model and model.strip() else get_default_model_key()

    try:
        yolo_model, used_model = load_model(model_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

    results_list = []
    for img_file in images:
        try:
            img = Image.open(img_file.file).convert("RGB")
        except Exception:
            raise HTTPException(status_code=400, detail=f"Failed to open image: {img_file.filename}")

        start = time.time()
        results = yolo_model(img)[0]
        duration_ms = (time.time() - start) * 1000
        track_latency(duration_ms)

        predictions = []
        for box in results.boxes:
            label = yolo_model.names[int(box.cls[0])]
            confidence = round(float(box.conf[0]), 2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            predictions.append({
                "label": label,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

        results_list.append({
            "image": img_file.filename,
            "predictions": predictions
        })

    return {
        "model_used": used_model,
        "results": results_list
    }
