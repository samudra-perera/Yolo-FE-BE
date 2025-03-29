from fastapi import APIRouter
import os
from pathlib import Path
import json
from ultralytics import YOLO

router = APIRouter()

MODEL_DIRECTORY = Path(__file__).resolve().parent.parent.parent / "weights"
DEFAULT_MODEL_PATH = Path("default_model.txt")
MODEL_METADATA_FILE = Path("model_metadata.json")


# Load metadata from JSON file
def load_metadata():
    if MODEL_METADATA_FILE.exists():
        with open(MODEL_METADATA_FILE, "r") as f:
            return json.load(f)
    return {}


@router.get("/management/models")
def list_models():
    try:
        metadata = load_metadata()
        model_names = list(metadata.keys())
        return {"available_models": model_names}
    except Exception as e:
        return {"available_models": [], "error": str(e)}


@router.get("/management/models/{model}/describe")
def describe_model(model: str):
    try:
        metadata = load_metadata()

        # Match using model name without file extension
        model_metadata = metadata.get(model)

        if not model_metadata:
            return {"error": f"No metadata found for model '{model}'"}

        # Return only required fields in the correct format
        return {
            "model": model_metadata["model"],
            "config": model_metadata["config"],
            "date_registered": model_metadata["date_registered"],
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/management/models/{model}/set-default")
def set_default_model(model: str):
    try:
        metadata = load_metadata()
        model_key = os.path.splitext(model)[0]

        if model_key not in metadata:
            return {
                "success": False,
                "error": f"Model '{model_key}' not found in metadata.",
            }

        # Save as default model
        DEFAULT_MODEL_PATH.write_text(model_key)
        return {"success": True, "default_model": model_key}

    except Exception as e:
        return {"success": False, "error": str(e)}
