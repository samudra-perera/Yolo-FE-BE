from typing import List, Dict

# Simulated model store
_models = {
    "model_0": {
        "config": {
            "input_size": [640, 640],
            "batch_size": 16,
            "confidence_threshold": 0.25,
        },
        "date_registered": "2025-03-15",
    },
    "model_1": {
        "config": {
            "input_size": [416, 416],
            "batch_size": 8,
            "confidence_threshold": 0.3,
        },
        "date_registered": "2025-03-20",
    },
    "model_2": {
        "config": {
            "input_size": [320, 320],
            "batch_size": 4,
            "confidence_threshold": 0.2,
        },
        "date_registered": "2025-03-22",
    },
}

_default_model = "model_0"


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
    _default_model = model


def get_default_model() -> str:
    return _default_model
