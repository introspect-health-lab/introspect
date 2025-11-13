# introspect - AI-Powered Malaria Diagnostics & Surveillance System

**introspect** is an edge AI-powered malaria diagnostics and surveillance platform built with Clean Architecture principles. It supports blood smear image analysis using YOLOv11 on Raspberry Pi 5, patient management, and real-time surveillance dashboards for malaria outbreak monitoring.

## 🎯 Project Overview

This system enables:
- **Edge AI Diagnostics**: YOLOv11-powered malaria detection on Raspberry Pi 5 with Camera Module 3
- **Dual Input Modes**: Direct camera capture or image upload for maximum flexibility
- **Patient Management**: Track patient information and test history
- **Surveillance Dashboard**: Monitor malaria cases by district, clinic, and time period
- **Offline-First**: Full functionality without internet connectivity, with sync capability
- **Web Interface**: Complete web UI with authentication and role-based access
- **RESTful API**: Designed for integration with mobile/web frontends

## 🏗️ Architecture

Built using **Clean Architecture** principles:

### Domain Layer (`src/entities/`)
Core business entities:
- `Patient` - Patient demographics and information
- `TestResult` - Malaria test results with AI analysis metadata
- `Clinic` - Health facility information
- `User` - Health workers and administrators

### Application Layer (`src/*/service.py`)
Business logic services:
- Patient management
- Test result processing
- AI inference integration
- Dashboard analytics
- Sync service for offline capability

### Infrastructure Layer (`src/infrastructure/`)
External services and integrations:
- `ai_inference.py` - YOLOv11 model inference for malaria detection
- `camera_service.py` - Raspberry Pi Camera Module 3 integration
- `file_storage.py` - Blood smear image storage
- `sync_service.py` - Offline synchronization

### Presentation Layer (`src/*/controller.py`)
FastAPI REST endpoints:
- `/api/auth` - Authentication (JWT)
- `/api/patients` - Patient CRUD operations
- `/api/results/analyze` - Upload and analyze blood smear images
- `/api/results/capture-and-analyze` - Capture from camera and analyze
- `/api/clinics` - Clinic management
- `/api/dashboard` - Surveillance analytics
- `/api/sync` - Offline sync operations

## 🚀 Quick Start

See **`QUICK_START.md`** for detailed setup instructions.

### Prerequisites
- Python 3.11+
- (Optional) Raspberry Pi 5 with Camera Module 3 for edge AI
- (Optional) Docker & Docker Compose for PostgreSQL

### Installation

```bash
# Clone repository
git clone <repository-url>
cd introspect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python create_tables.py

# Start application
uvicorn src.main:app --reload
```

Access the application at: **http://localhost:8000**

### 📚 Documentation

- **`QUICK_START.md`** - Get started in 5 minutes
- **`EDGE_AI_INTEGRATION_SUMMARY.md`** - Complete implementation overview
- **`RASPBERRY_PI_SETUP.md`** - Raspberry Pi 5 deployment guide
- **`LOGO_SETUP.md`** - Logo integration instructions
- **`models/README.md`** - YOLOv11 model documentation

### API Documentation

Interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Core Features

### 1. Edge AI Malaria Detection

**Camera Capture Mode** (Raspberry Pi 5):
```bash
POST /api/results/capture-and-analyze
```
- Captures image directly from Camera Module 3
- Runs YOLOv11 inference on-device
- No internet required
- Instant results

**Upload Mode** (Any device):
```bash
POST /api/results/analyze
```
- Upload blood smear images
- YOLOv11 malaria parasite detection
- Confidence scores and bounding boxes
- Automatic test result record creation

Both modes return:
- Detection result (Positive/Negative/Inconclusive)
- Confidence score
- Processing time
- Detailed detection metadata

### 2. Patient Management
```bash
GET    /api/patients          # List all patients
POST   /api/patients          # Create new patient
GET    /api/patients/{id}     # Get patient details
PUT    /api/patients/{id}     # Update patient
DELETE /api/patients/{id}     # Delete patient
GET    /api/patients/search   # Search by name or ID
```

### 3. Test Results
```bash
GET /api/results              # List results (with filters)
GET /api/results/{id}         # Get specific result
PUT /api/results/{id}         # Update result
GET /api/results/pending-sync # Get unsynced results
```

### 4. Surveillance Dashboard
```bash
GET /api/dashboard            # Complete dashboard data
GET /api/dashboard/districts  # District-level statistics
GET /api/dashboard/clinics    # Clinic-level statistics
```

### 5. Offline Sync
```bash
POST /api/sync/all           # Sync all pending results
POST /api/sync/retry         # Retry failed syncs
GET  /api/sync/status        # Get sync status
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register a user**
```bash
POST /auth/register
{
  "email": "healthworker@clinic.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

2. **Login to get token**
```bash
POST /auth/token
Form data:
  username: healthworker@clinic.com
  password: secure_password
```

3. **Use token in requests**
```bash
Authorization: Bearer <your_token>
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_patients_service.py
```

## 📁 Project Structure

```
clean-architecture/
├── src/
│   ├── entities/          # Domain models (Patient, TestResult, etc.)
│   ├── infrastructure/    # External services (AI, storage, sync)
│   ├── auth/             # Authentication service
│   ├── patients/         # Patient management
│   ├── results/          # Test results
│   ├── clinics/          # Clinic management
│   ├── dashboard/        # Analytics & surveillance
│   ├── sync/             # Offline sync
│   ├── frontend/         # Web UI templates
│   ├── database/         # Database configuration
│   ├── main.py           # FastAPI application
│   └── api.py            # Route registration
├── tests/                # Test suite
├── uploads/              # Uploaded images storage
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
# Database
DATABASE_URL=sqlite:///./introspect.db

# YOLOv11 Model
YOLO_MODEL_PATH=models/malaria_yolov11.pt
YOLO_CONFIDENCE_THRESHOLD=0.25
YOLO_IOU_THRESHOLD=0.45
YOLO_IMAGE_SIZE=640

# JWT Secret
SECRET_KEY=your-secret-key-here

# Optional: Central server for sync
CENTRAL_SERVER_URL=https://your-server.com
```

## 🤖 YOLOv11 Model Integration

### Adding Your Model

1. **Train YOLOv11 model** for malaria detection (see `models/README.md`)
2. **Place model file** in `models/malaria_yolov11.pt`
3. **Configure path** in `.env` file
4. **Restart application** - model loads automatically

### Model Training

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov11n.pt')

# Train on malaria dataset
results = model.train(
    data='data.yaml',
    epochs=100,
    imgsz=640
)

# Export for deployment
model.export(format='onnx')  # For Raspberry Pi
```

See `models/README.md` for detailed training instructions.

### Placeholder Mode

If no model is found, the system automatically uses placeholder mode:
- Generates random results for testing
- Perfect for development and UI testing
- No actual inference performed

## 🎨 Web Interface

Complete web UI included:
- **Landing Page** - Overview and features
- **Authentication** - Sign in/Sign up with JWT
- **Dashboard** - Surveillance analytics and statistics
- **Patient Management** - Add, view, edit patients
- **Analysis Page** - Dual input mode (camera + upload)
- **Results History** - View past test results
- **Responsive Design** - Works on desktop and mobile

## 📱 API Integration

The RESTful API supports integration with:
- Flutter mobile apps
- React/Vue/Angular web apps
- Third-party systems
- IoT devices

Features:
- CORS enabled for cross-origin requests
- JSON responses
- JWT authentication
- File upload support
- Comprehensive error handling

## 🛣️ Roadmap

- [x] YOLOv11 integration for malaria detection
- [x] Raspberry Pi 5 + Camera Module 3 support
- [x] Dual input mode (camera + upload)
- [x] Web interface with authentication
- [ ] Image quality validation
- [ ] Batch analysis
- [ ] PDF report generation
- [ ] Enhanced offline sync with conflict resolution
- [ ] Real-time notifications for outbreak alerts
- [ ] Multi-language support
- [ ] Advanced analytics and ML insights
- [ ] Mobile app (Flutter)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Your License Here]

## 📞 Support

For questions or issues:
- Check documentation files
- Review API docs at `/docs`
- Open an issue on GitHub

---

**Built with ❤️ for malaria elimination**
