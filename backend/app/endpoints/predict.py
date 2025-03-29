from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from pathlib import Path
import numpy as np
from PIL import Image
from ultralytics import YOLO
import onnxruntime as ort
import logging
import json
from app.services.onnx_postprocess import format_onnx_predictions

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "weights"
METADATA_FILE = Path(__file__).resolve().parent.parent.parent / "model_metadata.json"
DEFAULT_MODEL_KEY = "yolov8s_samudra_A100_best_torch"


def load_metadata():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}


def preprocess_image(img: Image.Image):
    img = np.array(img.resize((640, 640))).astype(np.float32)
    img = img / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img


def predict_onnx(img_array: np.ndarray, session: ort.InferenceSession):
    inputs = {session.get_inputs()[0].name: img_array}
    outputs = session.run(None, inputs)
    return outputs[0]


@router.post("/predict")
async def predict(image: UploadFile = File(...), model: str = Form(default=None)):
    metadata = load_metadata()
    model_key = model if model else DEFAULT_MODEL_KEY

    if model_key not in metadata:
        raise HTTPException(
            status_code=404, detail=f"Model '{model_key}' not found in metadata."
        )

    model_filename = metadata[model_key]["model"]
    model_path = MODEL_DIR / model_filename

    if not model_path.exists():
        raise HTTPException(
            status_code=404, detail=f"Model file '{model_filename}' not found."
        )

    img = Image.open(image.file).convert("RGB")

    if model_filename.endswith(".pt"):
        yolo_model = YOLO(str(model_path))
        results = yolo_model(img)[0]

        predictions = []
        for box in results.boxes:
            label = yolo_model.names[int(box.cls[0])]
            confidence = round(float(box.conf[0]), 2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            predictions.append(
                {"label": label, "confidence": confidence, "bbox": [x1, y1, x2, y2]}
            )

        return {"predictions": predictions, "model_used": model_key}

    elif model_filename.endswith(".onnx"):
        session = ort.InferenceSession(str(model_path))
        preprocessed = preprocess_image(img)
        raw_output = predict_onnx(preprocessed, session)
        formatted = format_onnx_predictions(raw_output, model_name=model_key)
        return formatted

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported model format. Only .pt and .onnx are supported.",
        )
