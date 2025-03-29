from ultralytics import YOLO

model = YOLO("weights/yolov8s_samudra_A100_best.pt")

model.export(format="onnx")
