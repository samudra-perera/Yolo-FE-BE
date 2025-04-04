from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
import numpy as np
import io
from PIL import Image
from ultralytics import YOLO
import os
import json
from app.services.model_registry import get_model, get_default_model

router = APIRouter()

def read_yolo_label_txt(label_file: UploadFile):
    labels = []
    for line in label_file.file:
        parts = line.decode().strip().split()
        if len(parts) != 5:
            continue
        cls, x_center, y_center, width, height = map(float, parts)
        labels.append({
            "class": int(cls),
            "bbox": [x_center, y_center, width, height]
        })
    return labels

def yolo_to_xyxy(bbox, img_width, img_height):
    x_center, y_center, w, h = bbox
    x1 = (x_center - w / 2) * img_width
    y1 = (y_center - h / 2) * img_height
    x2 = (x_center + w / 2) * img_width
    y2 = (y_center + h / 2) * img_height
    return [x1, y1, x2, y2]

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area else 0.0

def evaluate_predictions(preds, labels, iou_threshold=0.5):
    matched = set()
    tp = 0
    fp = 0
    for pred in preds:
        best_iou = 0
        best_idx = -1
        for idx, label in enumerate(labels):
            if idx in matched:
                continue
            iou = compute_iou(pred["bbox"], label["bbox"])
            if iou > best_iou:
                best_iou = iou
                best_idx = idx
        if best_iou >= iou_threshold:
            matched.add(best_idx)
            tp += 1
        else:
            fp += 1
    fn = len(labels) - len(matched)
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    return precision, recall

@router.post("/evaluate")
async def evaluate(
    images: List[UploadFile] = File(...),
    labels: List[UploadFile] = File(...),
    model: Optional[str] = Form(None),
    iou_threshold: float = Form(0.5),
):
    model_key = model or get_default_model()
    yolo_model = get_model(model_key)

    results = []
    precisions = []
    recalls = []

    for img_file, label_file in zip(images, labels):
        image = Image.open(io.BytesIO(await img_file.read())).convert("RGB")
        img_array = np.array(image)
        img_width, img_height = image.size

        gt_labels_raw = read_yolo_label_txt(label_file)
        gt_labels = [
            {
                "class": label["class"],
                "bbox": yolo_to_xyxy(label["bbox"], img_width, img_height)
            }
            for label in gt_labels_raw
        ]

        pred_results = yolo_model.predict(img_array, conf=0.25)[0]
        pred_boxes = pred_results.boxes.xyxy.cpu().numpy()
        pred_confs = pred_results.boxes.conf.cpu().numpy()
        pred_classes = pred_results.boxes.cls.cpu().numpy()

        predictions = []
        for box, conf, cls in zip(pred_boxes, pred_confs, pred_classes):
            predictions.append({
                "label": yolo_model.names[int(cls)],
                "confidence": float(conf),
                "bbox": list(map(float, box))
            })

        precision, recall = evaluate_predictions(
            [{"bbox": p["bbox"]} for p in predictions], gt_labels, iou_threshold
        )
        precisions.append(precision)
        recalls.append(recall)

        results.append({
            "image": img_file.filename,
            "precision": precision,
            "recall": recall,
            "predictions": predictions
        })

    mean_ap = sum(precisions) / len(precisions) if precisions else 0

    return {
        "model_used": model_key,
        "iou_threshold": iou_threshold,
        "aggregate": {
            "mAP": mean_ap,
            "precision": sum(precisions) / len(precisions),
            "recall": sum(recalls) / len(recalls),
        },
        "per_image": results,
    }
