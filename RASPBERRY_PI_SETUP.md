# Raspberry Pi 5 Setup Guide for Introspect

This guide will help you set up Introspect on a Raspberry Pi 5 with Camera Module 3 for edge AI malaria diagnostics using YOLOv11.

## 🎯 Overview

The Raspberry Pi 5 deployment enables:
- **Edge AI Processing**: Run YOLOv11 inference locally without cloud dependency
- **Camera Integration**: Direct capture from Raspberry Pi Camera Module 3
- **Offline Operation**: Full functionality without internet connectivity
- **Sync Capability**: Sync results to central server when connected

## 📋 Hardware Requirements

- **Raspberry Pi 5** (4GB or 8GB RAM recommended)
- **Raspberry Pi Camera Module 3** (or Camera Module 3 Wide)
- **MicroSD Card** (32GB or larger, Class 10 or better)
- **Power Supply** (Official Raspberry Pi 5 27W USB-C power supply)
- **Optional**: Cooling fan or heatsink for sustained AI workloads

## 🔧 Software Requirements

- **Raspberry Pi OS** (64-bit, Bookworm or later)
- **Python 3.11+**
- **YOLOv11 Model** (trained for malaria detection)

## 📦 Installation Steps

### 1. Prepare Raspberry Pi OS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv git libcap-dev
sudo apt install -y python3-opencv python3-picamera2

# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options -> Camera -> Enable
```

### 2. Clone and Setup Introspect

```bash
# Clone repository
cd ~
git clone <your-repo-url> introspect
cd introspect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install picamera2 (if not already installed system-wide)
pip install picamera2
```

### 3. Install YOLOv11 Dependencies

```bash
# Install PyTorch for Raspberry Pi (CPU version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install Ultralytics (YOLOv11)
pip install ultralytics

# For better performance, install ONNX Runtime
pip install onnxruntime
```

### 4. Add Your YOLOv11 Model

```bash
# Create models directory
mkdir -p models

# Copy your trained YOLOv11 model
# Place your model file at: models/malaria_yolov11.pt
# Or set custom path in environment variable
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=sqlite:///./introspect.db

# YOLOv11 Configuration
YOLO_MODEL_PATH=models/malaria_yolov11.pt
YOLO_CONFIDENCE_THRESHOLD=0.25
YOLO_IOU_THRESHOLD=0.45
YOLO_IMAGE_SIZE=640

# JWT Secret (generate a secure random string)
SECRET_KEY=your-secret-key-here

# Optional: Central server for sync
CENTRAL_SERVER_URL=https://your-central-server.com
```

### 6. Initialize Database

```bash
# Create database tables
python create_tables.py

# Optional: Seed with sample data
python seed_data.py
```

### 7. Test Camera

```bash
# Test camera capture
python3 << EOF
from picamera2 import Picamera2
camera = Picamera2()
camera.start()
camera.capture_file("test.jpg")
camera.stop()
print("Camera test successful! Check test.jpg")
EOF
```

### 8. Start the Application

```bash
# Development mode
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode (recommended)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### 9. Access the Application

Open a browser and navigate to:
- **Local**: `http://localhost:8000`
- **Network**: `http://<raspberry-pi-ip>:8000`

## 🚀 Usage

### Camera Capture Mode

1. Navigate to **Analyze** page
2. Select **"Capture from Camera"** option
3. Choose patient
4. Click **"Analyze"** button
5. The system will:
   - Capture image from Camera Module 3
   - Run YOLOv11 inference locally
   - Display results immediately
   - Save to database for later sync

### Upload Mode

1. Navigate to **Analyze** page
2. Select **"Upload Image"** option
3. Choose patient and upload image
4. Click **"Analyze"** button

## ⚙️ Performance Optimization

### 1. Use ONNX for Faster Inference

Convert your YOLOv11 model to ONNX format:

```bash
# Convert model (run on development machine)
from ultralytics import YOLO
model = YOLO('models/malaria_yolov11.pt')
model.export(format='onnx')
```

Update `.env`:
```bash
YOLO_MODEL_PATH=models/malaria_yolov11.onnx
```

### 2. Optimize Image Size

Reduce inference time by using smaller image size:
```bash
YOLO_IMAGE_SIZE=416  # Instead of 640
```

### 3. Enable Swap (for 4GB models)

```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set: CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## 🔄 Offline Sync

The system automatically tracks sync status. When internet is available:

```bash
# Sync all pending results
curl -X POST http://localhost:8000/api/sync/all \
  -H "Authorization: Bearer <your-token>"
```

Or use the web interface: **Dashboard → Sync Status**

## 🐛 Troubleshooting

### Camera Not Detected

```bash
# Check camera connection
libcamera-hello

# If not working, check cable and enable legacy camera
sudo raspi-config
# Interface Options -> Legacy Camera -> Enable
```

### Out of Memory Errors

- Use smaller YOLO model (yolov11n instead of yolov11x)
- Reduce image size in configuration
- Enable swap memory
- Close other applications

### Slow Inference

- Convert model to ONNX format
- Use INT8 quantization
- Reduce image size
- Consider using Coral USB Accelerator

## 📊 Model Training

To train your own YOLOv11 model for malaria detection:

1. Prepare dataset with annotated blood smear images
2. Use Ultralytics training pipeline
3. Export to `.pt` or `.onnx` format
4. Place in `models/` directory

See `TRAINING_GUIDE.md` for detailed instructions (coming soon).

## 🔐 Security Considerations

- Change default SECRET_KEY in production
- Use HTTPS with reverse proxy (nginx)
- Restrict network access with firewall
- Regular security updates

## 📝 Systemd Service (Auto-start)

Create `/etc/systemd/system/introspect.service`:

```ini
[Unit]
Description=Introspect Malaria Diagnostics
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/introspect
Environment="PATH=/home/pi/introspect/venv/bin"
ExecStart=/home/pi/introspect/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable introspect
sudo systemctl start introspect
sudo systemctl status introspect
```

## 📞 Support

For issues or questions:
- Check logs: `journalctl -u introspect -f`
- Review API docs: `http://<pi-ip>:8000/docs`
- GitHub Issues: [Your repo URL]

## 🎉 Next Steps

- Train custom YOLOv11 model with your malaria dataset
- Configure sync with central server
- Set up automated backups
- Deploy to multiple field locations

