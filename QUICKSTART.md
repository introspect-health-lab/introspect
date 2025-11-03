# Introspect - Quick Start Guide

Get up and running with the Introspect malaria diagnostics system in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Docker Desktop (optional, for PostgreSQL)
- A REST client (Postman, curl, or use the Swagger UI)

## Option 1: Quick Start with SQLite (Recommended for Testing)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### 3. Access the API Documentation

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Create Your First User

Using the Swagger UI or curl:

```bash
curl -X POST "http://localhost:8000/auth/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@introspect.com",
    "password": "SecurePassword123",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

### 5. Login to Get Access Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@introspect.com&password=SecurePassword123"
```

Save the `access_token` from the response. You'll need it for all subsequent requests.

### 6. Create a Clinic

```bash
curl -X POST "http://localhost:8000/api/clinics" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Central Health Clinic",
    "district": "Gaborone",
    "region": "South-East",
    "latitude": -24.6282,
    "longitude": 25.9231,
    "contact_phone": "+267 1234567"
  }'
```

Save the `id` from the response - this is your `clinic_id`.

### 7. Create a Patient

```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "clinic_id": "YOUR_CLINIC_ID_HERE",
    "first_name": "John",
    "last_name": "Doe",
    "age": 35,
    "gender": "male",
    "national_id": "123456789",
    "village": "Mogoditshane",
    "district": "Gaborone"
  }'
```

Save the `id` from the response - this is your `patient_id`.

### 8. Analyze a Blood Smear Image

Create a test image or use any image file:

```bash
curl -X POST "http://localhost:8000/api/results/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "image=@/path/to/blood_smear.jpg" \
  -F "patient_id=YOUR_PATIENT_ID_HERE" \
  -F "clinic_id=YOUR_CLINIC_ID_HERE" \
  -F "notes=Patient reports fever" \
  -F "symptoms=fever,chills,headache"
```

You'll receive an analysis result with:
- Test result (positive/negative/inconclusive)
- Confidence score
- Processing time

### 9. View Dashboard

```bash
curl -X GET "http://localhost:8000/api/dashboard" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Option 2: Production Setup with Docker & PostgreSQL

### 1. Start All Services

```bash
docker compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Introspect API on port 8000

### 2. Follow Steps 3-9 from Option 1

The API endpoints are the same, just use `http://localhost:8000` as the base URL.

### 3. Stop Services

```bash
docker compose down
```

---

## Using the Swagger UI (Easiest Method)

1. Navigate to http://localhost:8000/docs
2. Click on "Authorize" button (top right)
3. First, use the `/auth/` endpoint to register a user
4. Then use `/auth/token` to login and get a token
5. Click "Authorize" again and paste your token
6. Now you can test all endpoints directly from the browser!

---

## Sample Workflow

Here's a complete workflow for testing the system:

### 1. Setup (One-time)
```bash
# Register user
POST /auth/

# Login
POST /auth/token

# Create clinic
POST /api/clinics
```

### 2. Daily Operations
```bash
# Create patient (or search existing)
POST /api/patients
# or
GET /api/patients/search?q=John

# Upload and analyze blood smear
POST /api/results/analyze

# View results
GET /api/results?patient_id=XXX

# Check dashboard
GET /api/dashboard
```

### 3. Sync (for offline scenarios)
```bash
# Check sync status
GET /api/sync/status

# Sync pending results
POST /api/sync/all

# Retry failed syncs
POST /api/sync/retry
```

---

## Testing the AI Inference

The current implementation uses a **placeholder AI model** that generates random results for demonstration. To test:

1. Upload any image file (JPEG or PNG)
2. The system will:
   - Validate the image
   - Simulate AI processing
   - Return a random result (positive/negative/inconclusive)
   - Store the result in the database

**Note**: In production, replace the placeholder in `src/infrastructure/ai_inference.py` with a real TensorFlow Lite model.

---

## Troubleshooting

### Database Connection Error
If using Docker and getting connection errors:
```bash
# Wait for PostgreSQL to be ready
docker compose logs db

# Restart the API service
docker compose restart api
```

### Port Already in Use
If port 8000 is already in use:
```bash
# Option 1: Stop the conflicting service
# Option 2: Change the port in docker-compose.yml or when running uvicorn
uvicorn src.main:app --reload --port 8001
```

### Import Errors
Make sure you're in the project root directory and have installed all dependencies:
```bash
pip install -r requirements.txt
```

### SQLite Database Locked
If you get database locked errors with SQLite:
```bash
# Stop all running instances
# Delete the database file
rm introspect.db test.db

# Restart the server
uvicorn src.main:app --reload
```

---

## Next Steps

1. **Explore the API**: Use the Swagger UI to test all endpoints
2. **Check the Dashboard**: View aggregated statistics
3. **Test Offline Sync**: Create results and test the sync functionality
4. **Read the Full Documentation**: See README.md and API_DOCUMENTATION.md
5. **Run Tests**: Execute `pytest` to run the test suite
6. **Integrate with Flutter**: Use the API endpoints in your Flutter app

---

## Sample Data Script

Want to populate the database with sample data? Create a file `seed_data.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Register and login
response = requests.post(f"{BASE_URL}/auth/", json={
    "email": "demo@introspect.com",
    "password": "Demo123!",
    "first_name": "Demo",
    "last_name": "User"
})

response = requests.post(f"{BASE_URL}/auth/token", data={
    "username": "demo@introspect.com",
    "password": "Demo123!"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create clinics
clinics = []
for name, district in [("Central Clinic", "Gaborone"), ("North Clinic", "Francistown")]:
    response = requests.post(f"{BASE_URL}/api/clinics", headers=headers, json={
        "name": name,
        "district": district,
        "region": "South-East" if district == "Gaborone" else "North-East"
    })
    clinics.append(response.json()["id"])

print(f"Created {len(clinics)} clinics")
print("Sample data loaded successfully!")
```

Run it with: `python seed_data.py`

---

## Support

For issues or questions:
- Check the full documentation in README.md
- Review API_DOCUMENTATION.md for endpoint details
- Open an issue on GitHub
- Contact the development team

Happy diagnosing! 🔬

