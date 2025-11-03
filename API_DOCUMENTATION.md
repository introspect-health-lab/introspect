# Introspect API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All endpoints (except `/auth/register` and `/auth/token`) require JWT authentication.

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using Authentication
Include the token in the Authorization header:
```http
Authorization: Bearer <your_token>
```

---

## Clinics

### Create Clinic
```http
POST /api/clinics
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Central Health Clinic",
  "district": "Gaborone",
  "region": "South-East",
  "latitude": -24.6282,
  "longitude": 25.9231,
  "contact_phone": "+267 1234567",
  "contact_email": "clinic@example.com"
}
```

### List Clinics
```http
GET /api/clinics?district=Gaborone
Authorization: Bearer <token>
```

### Get Clinic
```http
GET /api/clinics/{clinic_id}
Authorization: Bearer <token>
```

### Update Clinic
```http
PUT /api/clinics/{clinic_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "contact_phone": "+267 7654321"
}
```

### Delete Clinic
```http
DELETE /api/clinics/{clinic_id}
Authorization: Bearer <token>
```

---

## Patients

### Create Patient
```http
POST /api/patients
Authorization: Bearer <token>
Content-Type: application/json

{
  "clinic_id": "123e4567-e89b-12d3-a456-426614174000",
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "age": 33,
  "gender": "female",
  "phone_number": "+267 71234567",
  "national_id": "123456789",
  "village": "Mogoditshane",
  "district": "Gaborone"
}
```

**Gender values:** `male`, `female`, `other`

### List Patients
```http
GET /api/patients?clinic_id={clinic_id}
Authorization: Bearer <token>
```

### Search Patients
```http
GET /api/patients/search?q=Jane&clinic_id={clinic_id}
Authorization: Bearer <token>
```

### Get Patient
```http
GET /api/patients/{patient_id}
Authorization: Bearer <token>
```

### Update Patient
```http
PUT /api/patients/{patient_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone_number": "+267 72345678",
  "village": "Tlokweng"
}
```

### Delete Patient
```http
DELETE /api/patients/{patient_id}
Authorization: Bearer <token>
```

---

## Test Results & Analysis

### Analyze Blood Smear Image
Upload an image and get AI analysis results.

```http
POST /api/results/analyze
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>
patient_id: 123e4567-e89b-12d3-a456-426614174000
clinic_id: 123e4567-e89b-12d3-a456-426614174001
notes: Patient reports fever and chills
symptoms: fever,chills,headache
```

**Response:**
```json
{
  "test_result_id": "123e4567-e89b-12d3-a456-426614174002",
  "result": "positive",
  "confidence_score": 0.92,
  "processing_time_ms": 245.3,
  "message": "Analysis complete: positive"
}
```

**Result values:** `positive`, `negative`, `inconclusive`

### List Test Results
```http
GET /api/results?clinic_id={clinic_id}&patient_id={patient_id}&status=positive
Authorization: Bearer <token>
```

**Query Parameters:**
- `clinic_id` (optional): Filter by clinic
- `patient_id` (optional): Filter by patient
- `status` (optional): Filter by result status (positive/negative/inconclusive)

### Get Test Result
```http
GET /api/results/{result_id}
Authorization: Bearer <token>
```

### Update Test Result
```http
PUT /api/results/{result_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "notes": "Updated notes after review",
  "result": "positive"
}
```

### Get Pending Sync Results
```http
GET /api/results/pending-sync
Authorization: Bearer <token>
```

### Mark Result as Synced
```http
POST /api/results/{result_id}/sync
Authorization: Bearer <token>
```

---

## Dashboard & Analytics

### Get Dashboard Data
```http
GET /api/dashboard?days=30&district=Gaborone
Authorization: Bearer <token>
```

**Query Parameters:**
- `days` (default: 30): Number of days for time series data
- `district` (optional): Filter by district

**Response:**
```json
{
  "summary": {
    "total_tests": 1250,
    "total_positive": 125,
    "total_negative": 1100,
    "total_inconclusive": 25,
    "overall_positivity_rate": 10.0,
    "total_patients": 980,
    "total_clinics": 15,
    "total_health_workers": 45,
    "last_updated": "2025-11-02T10:30:00Z"
  },
  "district_stats": [
    {
      "district": "Gaborone",
      "total_tests": 500,
      "positive_cases": 50,
      "negative_cases": 440,
      "inconclusive_cases": 10,
      "positivity_rate": 10.0,
      "clinics_count": 5
    }
  ],
  "recent_tests": 85,
  "time_series": [
    {
      "date": "2025-10-01",
      "positive_cases": 5,
      "negative_cases": 45,
      "total_tests": 50
    }
  ]
}
```

### Get District Statistics
```http
GET /api/dashboard/districts?district=Gaborone
Authorization: Bearer <token>
```

### Get Clinic Statistics
```http
GET /api/dashboard/clinics?district=Gaborone
Authorization: Bearer <token>
```

---

## Sync Operations

### Sync All Pending Results
```http
POST /api/sync/all
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total": 15,
  "synced": 14,
  "failed": 1
}
```

### Retry Failed Syncs
```http
POST /api/sync/retry
Authorization: Bearer <token>
```

### Get Sync Status
```http
GET /api/sync/status
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_results": 1250,
  "pending": 15,
  "synced": 1230,
  "failed": 5,
  "sync_percentage": 98.4
}
```

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Data Models

### Patient
```json
{
  "id": "uuid",
  "clinic_id": "uuid",
  "first_name": "string",
  "last_name": "string",
  "date_of_birth": "date",
  "age": "integer",
  "gender": "male|female|other",
  "phone_number": "string",
  "national_id": "string",
  "village": "string",
  "district": "string"
}
```

### Test Result
```json
{
  "id": "uuid",
  "patient_id": "uuid",
  "clinic_id": "uuid",
  "health_worker_id": "uuid",
  "test_date": "datetime",
  "result": "positive|negative|inconclusive",
  "confidence_score": "float (0-1)",
  "image_path": "string",
  "image_filename": "string",
  "model_version": "string",
  "processing_time_ms": "float",
  "notes": "string",
  "symptoms": "string",
  "sync_status": "pending|synced|failed",
  "synced_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Clinic
```json
{
  "id": "uuid",
  "name": "string",
  "district": "string",
  "region": "string",
  "latitude": "float",
  "longitude": "float",
  "contact_phone": "string",
  "contact_email": "string"
}
```

