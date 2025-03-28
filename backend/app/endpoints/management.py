from fastapi import APIRouter, HTTPException
from app.services import model_registry

router = APIRouter()


@router.get("/management/models")
def get_models():
    return {"available_models": model_registry.list_models()}


@router.get("/management/models/{model}/describe")
def describe_model(model: str):
    if model not in model_registry.list_models():
        raise HTTPException(status_code=404, detail="Model not found")
    return model_registry.get_model_details(model)


@router.get("/management/models/{model}/set-default")
def set_default(model: str):
    if model not in model_registry.list_models():
        raise HTTPException(status_code=404, detail="Model not found")
    model_registry.set_default_model(model)
    return {"success": True, "default_model": model}
