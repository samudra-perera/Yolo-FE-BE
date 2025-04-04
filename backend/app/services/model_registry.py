from typing import List, Dict
from pathlib import Path
import json
from ultralytics import YOLO

# Simulated model store
_models = {
    "best_model_v4": {
        "config": {
            "input_size": [640, 640],
            "batch_size": 16,
            "confidence_threshold": 0.25,
        },
        "date_registered": "2025-03-14",
    },
    "best_model_v5": {
        "config": {
            "input_size": [640, 640],
            "batch_size": 16,
            "confidence_threshold": 0.25,
        },
        "date_registered": "2025-03-27",
    },
    "best_model_v6": {
        "config": {
            "input_size": [640, 640],
            "batch_size": 16,
            "confidence_threshold": 0.25,
        },
        "date_registered": "2025-03-21",
    },
}

_default_model = "best_model_v6"

WEIGHTS_DIR = Path(__file__).resolve().parent.parent.parent / "weights"
MODEL_METADATA_FILE = Path(__file__).resolve().parent.parent.parent / "model_metadata.json"

def list_models() -> List[str]:
    return list(_models.keys())

def get_model_details(model: str) -> Dict:
    return {
        "model": model,
        "config": _models[model]["config"],
        "date_registered": _models[model]["date_registered"],
    }

def set_default_model(model: str):
    global _default_model
    if model in _models:
        _default_model = model
    else:
        raise ValueError(f"Model '{model}' not found.")

def get_default_model() -> str:
    return _default_model

def get_model(model_key: str) -> YOLO:
    if not MODEL_METADATA_FILE.exists():
        raise ValueError("Model metadata file not found.")

    with open(MODEL_METADATA_FILE, "r") as f:
        metadata = json.load(f)

    if model_key not in metadata:
        raise ValueError(f"Model '{model_key}' not found in metadata.")

    model_file = metadata[model_key]["model"]
    model_path = WEIGHTS_DIR / model_file

    if not model_path.exists():
        raise ValueError(f"Model file '{model_path}' does not exist.")

    return YOLO(str(model_path))
