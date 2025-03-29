import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import os

# Absolute path to the model
model_path = os.path.join("weights", "yolov8s_samudra_A100_best.onnx")
onnx_session = ort.InferenceSession(model_path)


def preprocess_image(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((640, 640))
    img_np = np.array(img).astype(np.float32)
    img_np = img_np.transpose(2, 0, 1) / 255.0
    img_np = np.expand_dims(img_np, axis=0)
    return img_np


def run_inference(image_bytes: bytes):
    input_data = preprocess_image(image_bytes)
    input_name = onnx_session.get_inputs()[0].name
    output = onnx_session.run(None, {input_name: input_data})[0]
    return output.tolist()
