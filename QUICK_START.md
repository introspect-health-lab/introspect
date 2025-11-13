# Quick Start Guide - Introspect with Edge AI

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11+
- Git
- (Optional) Raspberry Pi 5 with Camera Module 3

### Step 1: Clone and Install

```bash
# Clone repository
git clone <your-repo-url> introspect
cd introspect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
# Create database tables
python create_tables.py

# (Optional) Add sample data
python seed_data.py
```

### Step 3: Add Logo Image

Save your logo image as:
```
src/frontend/static/images/introspect-logo.png
```

See `LOGO_SETUP.md` for details.

### Step 4: Start Application

```bash
# Development mode
uvicorn src.main:app --reload

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Step 5: Access Web Interface

Open browser and navigate to:
```
http://localhost:8000
```

### Step 6: Create Account and Test

1. Click **"Sign Up"**
2. Create your account
3. Sign in
4. Add a patient
5. Go to **"Analyze"** page
6. Try both modes:
   - **Upload Image**: Works immediately (placeholder mode)
   - **Capture from Camera**: Requires Raspberry Pi setup

## 📱 Using the Application

### Upload Mode (Works Everywhere)

1. Select **"Upload Image"** option
2. Choose patient from dropdown
3. Upload blood smear image
4. Add notes/symptoms (optional)
5. Click **"Analyze"**
6. View results

### Camera Mode (Raspberry Pi Only)

1. Select **"Capture from Camera"** option
2. Choose patient from dropdown
3. Add notes/symptoms (optional)
4. Click **"Analyze"**
5. Image captured automatically
6. View results

## 🎯 Next Steps

### For Development/Testing
- Application works in placeholder mode
- No model or camera required
- Perfect for UI/UX testing

### For Production Deployment

1. **Add YOLOv11 Model**:
   ```bash
   # Place your trained model
   cp your_model.pt models/malaria_yolov11.pt
   ```

2. **Configure Environment**:
   ```bash
   # Create .env file
   cat > .env << EOF
   DATABASE_URL=sqlite:///./introspect.db
   YOLO_MODEL_PATH=models/malaria_yolov11.pt
   YOLO_CONFIDENCE_THRESHOLD=0.25
   SECRET_KEY=$(openssl rand -hex 32)
   EOF
   ```

3. **Deploy to Raspberry Pi**:
   - Follow `RASPBERRY_PI_SETUP.md`
   - Install picamera2
   - Connect Camera Module 3
   - Test camera capture

## 📚 Documentation

- **`EDGE_AI_INTEGRATION_SUMMARY.md`** - Complete implementation overview
- **`RASPBERRY_PI_SETUP.md`** - Detailed Raspberry Pi setup guide
- **`LOGO_SETUP.md`** - Logo integration instructions
- **`models/README.md`** - YOLOv11 model documentation

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# Database
DATABASE_URL=sqlite:///./introspect.db

# YOLOv11 Model (optional - uses placeholder if not set)
YOLO_MODEL_PATH=models/malaria_yolov11.pt
YOLO_CONFIDENCE_THRESHOLD=0.25
YOLO_IOU_THRESHOLD=0.45
YOLO_IMAGE_SIZE=640

# JWT Secret (required for production)
SECRET_KEY=your-secret-key-here

# Optional: Central server for sync
CENTRAL_SERVER_URL=https://your-server.com
```

### Generate Secret Key

```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🐛 Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database errors
```bash
# Recreate database
rm introspect.db
python create_tables.py
```

### Logo not showing
```bash
# Check file exists
ls -la src/frontend/static/images/introspect-logo.png

# Clear browser cache
# Press Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
```

### Camera not working
- Only works on Raspberry Pi with Camera Module 3
- Install picamera2: `pip install picamera2`
- Enable camera: `sudo raspi-config` → Interface Options → Camera
- Test: `libcamera-hello`

## 📊 API Documentation

Interactive API docs available at:
```
http://localhost:8000/docs
```

## 🎓 Training YOLOv11 Model

Quick training example:

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov11n.pt')

# Train on your dataset
results = model.train(
    data='data.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)

# Export for deployment
model.export(format='onnx')
```

See `models/README.md` for detailed training instructions.

## 🔐 Security Notes

For production:
- Change default SECRET_KEY
- Use HTTPS (nginx reverse proxy)
- Enable firewall
- Regular security updates
- Backup database regularly

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **Logs**: Check terminal output
- **Issues**: Review error messages in browser console (F12)

## ✅ Verification Checklist

- [ ] Application starts without errors
- [ ] Can access web interface
- [ ] Can create account and sign in
- [ ] Can add patients
- [ ] Upload mode works (placeholder results)
- [ ] Logo displays correctly
- [ ] API docs accessible at /docs

## 🎉 You're Ready!

The application is now running with:
- ✅ Dual input mode (camera + upload)
- ✅ YOLOv11 integration (placeholder mode)
- ✅ Camera service (mock mode)
- ✅ Complete web interface
- ✅ API endpoints

**Add your YOLOv11 model to enable real inference!**

For detailed setup on Raspberry Pi, see `RASPBERRY_PI_SETUP.md`.

