# AI Models Directory

This directory stores AI/ML models for malaria detection using YOLOv11.

## 📁 Model Files

Place your trained YOLOv11 model in this directory:

### Recommended Files
- `malaria_yolov11.pt` - PyTorch model (default)
- `malaria_yolov11.onnx` - ONNX model (optimized for Raspberry Pi)
- `malaria_yolov11_int8.tflite` - TensorFlow Lite INT8 quantized model

## 🎯 Model Requirements

Your YOLOv11 model should be trained to detect:
- **Malaria parasites** in blood smear images
- **Classes**: Typically `plasmodium` or specific species
- **Input**: RGB images (recommended 640x640)
- **Output**: Bounding boxes with confidence scores

## 🔧 Configuration

Set the model path in `.env` file:

```bash
YOLO_MODEL_PATH=models/malaria_yolov11.pt
YOLO_CONFIDENCE_THRESHOLD=0.25
YOLO_IOU_THRESHOLD=0.45
YOLO_IMAGE_SIZE=640
```

## 📊 Model Training

To train your own YOLOv11 model, see `RASPBERRY_PI_SETUP.md` for detailed instructions.

Quick start:
```python
from ultralytics import YOLO

model = YOLO('yolov11n.pt')
results = model.train(data='data.yaml', epochs=100, imgsz=640)
model.export(format='onnx')  # For Raspberry Pi deployment
```

## 📦 Placeholder Mode

If no model file is found, the system automatically falls back to **placeholder mode**:
- Generates random results for testing
- Useful for development and UI testing
- No actual inference performed

## 📝 Model Performance

| Model | Size | Inference Time (Pi 5) | Recommended Use |
|-------|------|----------------------|-----------------|
| YOLOv11n | 6MB | ~200ms | Edge devices |
| YOLOv11s | 22MB | ~400ms | Balanced |
| YOLOv11m | 50MB | ~800ms | High accuracy |

## 📞 Support

For model training assistance, see documentation or contact the development team.
