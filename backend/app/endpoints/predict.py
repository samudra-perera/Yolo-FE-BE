from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional

router = APIRouter()


# Simulated model inference
def dummy_yolo_inference(image: UploadFile, model: str):
    return {
        "predictions": [
            {"label": "timmies", "confidence": 0.91, "bbox": [42, 58, 172, 310]},
            {"label": "paper_cup", "confidence": 0.88, "bbox": [200, 120, 320, 250]},
        ],
        "model_used": model,
    }


@router.post("/predict")
async def predict(
    image: UploadFile = File(...),
    model: Optional[str] = Form("model_0"),  # default model
):
    result = dummy_yolo_inference(image, model)
    return JSONResponse(content=result)
