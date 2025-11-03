# Introspect - Malaria Diagnostics & Surveillance System

**Introspect** is an AI-powered malaria diagnostics and surveillance API built with Clean Architecture principles. It supports blood smear image analysis using AI models, patient management, and real-time surveillance dashboards for malaria outbreak monitoring.

## 🎯 Project Overview

This system enables:
- **AI-Powered Diagnostics**: Upload blood smear images (from OpenFlexure Microscope) and get instant malaria detection results
- **Patient Management**: Track patient information and test history
- **Surveillance Dashboard**: Monitor malaria cases by district, clinic, and time period
- **Offline-First**: Sync capability for areas with intermittent connectivity
- **Flutter Integration**: RESTful API designed for Flutter mobile/web frontends

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
- `ai_inference.py` - AI model inference (placeholder for TensorFlow Lite)
- `file_storage.py` - Blood smear image storage
- `sync_service.py` - Offline synchronization

### Presentation Layer (`src/*/controller.py`)
FastAPI REST endpoints:
- `/api/auth` - Authentication (JWT)
- `/api/patients` - Patient CRUD operations
- `/api/results` - Test results and analysis
- `/api/clinics` - Clinic management
- `/api/dashboard` - Surveillance analytics
- `/api/sync` - Offline sync operations

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for PostgreSQL)
- Or SQLite for local development

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd clean-architecture
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# For development (includes pytest)
pip install -r requirements-dev.txt
```

### Running the Application

#### Option 1: Docker with PostgreSQL (Production-like)
```bash
# Start all services (API + PostgreSQL)
docker compose up --build

# Stop services
docker compose down
```

The API will be available at `http://localhost:8000`

#### Option 2: Local Development with SQLite
```bash
# The default configuration uses SQLite (introspect.db)
uvicorn src.main:app --reload
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Core Features

### 1. Image Upload & Analysis
```bash
POST /api/results/analyze
```
Upload a blood smear image and receive:
- Malaria detection result (Positive/Negative/Inconclusive)
- AI confidence score
- Processing time
- Automatic test result record creation

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

### Database
Edit `src/database/core.py` to configure database:
- **SQLite** (default): `sqlite:///./introspect.db`
- **PostgreSQL**: Set `DATABASE_URL` environment variable

### Environment Variables
Create a `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/introspect
SECRET_KEY=your-secret-key-here
```

## 🤖 AI Model Integration

The current implementation includes a **placeholder AI inference service**. To integrate a real model:

1. Train or obtain a TensorFlow Lite model for malaria detection
2. Place the `.tflite` file in the project
3. Update `src/infrastructure/ai_inference.py`:
   - Uncomment TensorFlow Lite loading code
   - Configure model path
   - Adjust preprocessing for your model's requirements

## 📱 Flutter Frontend Integration

The API is designed for Flutter integration:
- CORS enabled for cross-origin requests
- RESTful endpoints with JSON responses
- JWT authentication
- File upload support for images
- Comprehensive error responses

## 🛣️ Roadmap

- [ ] Integrate real TensorFlow Lite malaria detection model
- [ ] Add image quality validation
- [ ] Implement batch analysis
- [ ] Add export functionality (PDF reports, CSV data)
- [ ] Enhanced offline sync with conflict resolution
- [ ] Real-time notifications for outbreak alerts
- [ ] Multi-language support
- [ ] Advanced analytics and ML insights
