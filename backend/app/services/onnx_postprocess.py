import numpy as np
import torch
from ultralytics.utils.ops import non_max_suppression

CLASS_NAMES = ["Coffee Cup", "Tims Cup"]


def format_onnx_predictions(
    onnx_output: np.ndarray, confidence_threshold=0.1, model_name="model_onnx"
):
    predictions = []

    # Convert ONNX (NumPy) to PyTorch Tensor
    preds = torch.tensor(onnx_output[0])

    # Apply Ultralytics' NMS (expects shape: (num_preds, 6) with [x1, y1, x2, y2, conf, cls])
    nms_results = non_max_suppression(
        preds.unsqueeze(0),  # Add batch dimension
        conf_thres=confidence_threshold,
        iou_thres=0.5,
    )[0]

    if nms_results is None or len(nms_results) == 0:
        return {"predictions": [], "model_used": model_name}

    for det in nms_results.cpu().numpy():
        x1, y1, x2, y2, conf, class_id = det
        class_id = int(class_id)
        if 0 <= class_id < len(CLASS_NAMES):
            predictions.append(
                {
                    "label": CLASS_NAMES[class_id],
                    "confidence": round(float(conf) * 100, 2),
                    "bbox": [
                        int(min(x1, x2)),
                        int(min(y1, y2)),
                        int(max(x1, x2)),
                        int(max(y1, y2)),
                    ],
                }
            )

    return {"predictions": predictions, "model_used": model_name}
