from ultralytics import YOLO
import onnxruntime as ort
from fastapi import APIRouter, File, UploadFile
import numpy as np
from PIL import Image
import cv2
from app.services.onnx_postprocess import format_onnx_predictions
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()
# Load PyTorch model
pt_model = YOLO("weights/yolov8s_samudra_A100_best.pt")

# Load ONNX model
onnx_session = ort.InferenceSession("weights/yolov8s_samudra_A100_best.onnx")


def preprocess_image(img: Image.Image):
    img = np.array(img.resize((640, 640))).astype(np.float32)
    img = img / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img


def predict_onnx(img_array: np.ndarray):
    inputs = {onnx_session.get_inputs()[0].name: img_array}
    outputs = onnx_session.run(None, inputs)
    return outputs[0]


@router.post("/predict")
async def predict_both(file: UploadFile = File(...)):
    img = Image.open(file.file).convert("RGB")
    preprocessed = preprocess_image(img)

    # PyTorch
    pt_result = pt_model(img)

    # ONNX
    onnx_result = predict_onnx(preprocessed)
    logging.debug(f"[ONNX] Raw output: {onnx_result}")  # <--- LOG HERE

    formatted = format_onnx_predictions(onnx_result)

    return {
        "pytorch_output": str(pt_result),
        "onnx_output": onnx_result.tolist(),
        "formatted_onnx": formatted,
    }
