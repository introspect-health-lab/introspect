# Migration Guide: Todo App → Introspect Malaria Diagnostics

This guide explains the changes made when repurposing the clean architecture template into the Introspect malaria diagnostics system.

## Overview of Changes

The project has been transformed from a simple todo management application to a comprehensive malaria diagnostics and surveillance system while maintaining the clean architecture principles.

## Database Schema Changes

### Removed Entities
- `Todo` - Replaced with malaria-specific entities

### Modified Entities

#### User Entity

```python
class User:
    id: UUID
    email: str
    first_name: str
    last_name: str
    password_hash: str
    role: UserRole  # NEW: health_worker, admin, supervisor
    clinic_id: UUID  # NEW: Associated clinic
    phone_number: str  # NEW
    is_active: bool  # NEW
```

### New Entities

#### Clinic
```python
class Clinic:
    id: UUID
    name: str
    district: str
    region: str
    latitude: float
    longitude: float
    contact_phone: str
    contact_email: str
```

#### Patient
```python
class Patient:
    id: UUID
    clinic_id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    age: int
    gender: Gender  # male, female, other
    phone_number: str
    national_id: str
    village: str
    district: str
```

#### TestResult
```python
class TestResult:
    id: UUID
    patient_id: UUID
    clinic_id: UUID
    health_worker_id: UUID
    test_date: datetime
    result: TestStatus  # positive, negative, inconclusive
    confidence_score: float
    image_path: str
    image_filename: str
    model_version: str
    processing_time_ms: float
    notes: str
    symptoms: str
    sync_status: SyncStatus  # pending, synced, failed
    synced_at: datetime
    created_at: datetime
    updated_at: datetime
```

## API Endpoint Changes

### Removed Endpoints
- `GET /todos/` → Replaced with results endpoints
- `POST /todos/` → Replaced with analysis endpoint
- `PUT /todos/{id}` → Replaced with results update
- `DELETE /todos/{id}` → Results are not deleted, only archived

### Modified Endpoints

#### Authentication (Unchanged)
- `POST /auth/` - Register user
- `POST /auth/token` - Login

#### Users (Unchanged)
- `GET /users/me` - Get current user

### New Endpoints

#### Clinics
- `POST /api/clinics` - Create clinic
- `GET /api/clinics` - List clinics
- `GET /api/clinics/{id}` - Get clinic
- `PUT /api/clinics/{id}` - Update clinic
- `DELETE /api/clinics/{id}` - Delete clinic

#### Patients
- `POST /api/patients` - Create patient
- `GET /api/patients` - List patients
- `GET /api/patients/search` - Search patients
- `GET /api/patients/{id}` - Get patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

#### Test Results & Analysis
- `POST /api/results/analyze` - Upload and analyze blood smear
- `GET /api/results` - List test results
- `GET /api/results/{id}` - Get test result
- `PUT /api/results/{id}` - Update test result
- `GET /api/results/pending-sync` - Get unsynced results
- `POST /api/results/{id}/sync` - Mark as synced

#### Dashboard
- `GET /api/dashboard` - Get dashboard data
- `GET /api/dashboard/districts` - District statistics
- `GET /api/dashboard/clinics` - Clinic statistics

#### Sync
- `POST /api/sync/all` - Sync all pending
- `POST /api/sync/retry` - Retry failed syncs
- `GET /api/sync/status` - Get sync status

## Code Structure Changes

### New Modules

```
src/
├── clinics/          # NEW: Clinic management
│   ├── controller.py
│   ├── models.py
│   └── service.py
├── patients/         # NEW: Patient management
│   ├── controller.py
│   ├── models.py
│   └── service.py
├── results/          # NEW: Test results (replaces todos)
│   ├── controller.py
│   ├── models.py
│   └── service.py
├── dashboard/        # NEW: Analytics and surveillance
│   ├── controller.py
│   ├── models.py
│   └── service.py
├── sync/             # NEW: Offline sync
│   └── controller.py
└── infrastructure/   # NEW: External services
    ├── ai_inference.py
    ├── file_storage.py
    └── sync_service.py
```

### Removed Modules
- `src/todos/` - Replaced with results module

## Configuration Changes

### requirements.txt
**Added:**
- `pillow` - Image processing
- `numpy` - Numerical operations
- `tensorflow-lite` - AI model inference
- `python-magic` - File type detection
- `aiofiles` - Async file operations

### docker-compose.yml
**Changed:**
- Database name: `db` → `introspect`
- Environment variable: `DATABASE_URL` points to `introspect` database

### main.py
**Added:**
- CORS middleware for Flutter integration
- New entity imports
- Updated app title and description

## Migration Steps

If you have an existing database with todo data:

### 1. Backup Your Data
```bash
# For SQLite
cp introspect.db introspect.db.backup

# For PostgreSQL
pg_dump -U postgres introspect > backup.sql
```

### 2. Clear Old Schema
```bash
# For SQLite
rm introspect.db

# For PostgreSQL
docker compose down -v
```

### 3. Start Fresh
```bash
# The new schema will be created automatically
uvicorn src.main:app --reload
# or
docker compose up --build
```

### 4. Migrate Users (Optional)
If you want to keep existing users:

```python
# migration_script.py
import sqlite3

# Connect to old and new databases
old_db = sqlite3.connect('introspect.db.backup')
new_db = sqlite3.connect('introspect.db')

# Copy users
old_cursor = old_db.cursor()
new_cursor = new_db.cursor()

users = old_cursor.execute("SELECT id, email, first_name, last_name, password_hash FROM users").fetchall()

for user in users:
    new_cursor.execute(
        "INSERT INTO users (id, email, first_name, last_name, password_hash, role, is_active) VALUES (?, ?, ?, ?, ?, 'health_worker', 1)",
        user
    )

new_db.commit()
print(f"Migrated {len(users)} users")
```

## Testing Changes

### New Test Files
- `tests/test_patients_service.py` - Patient service tests
- `tests/test_clinics_service.py` - Clinic service tests

### Updated Test Files
- `tests/conftest.py` - Updated to import new entities

### Removed Test Files
- `tests/test_todos_service.py` - Can be removed or kept as reference
- `tests/e2e/test_todos_endpoints.py` - Can be removed

## Frontend Changes

The web frontend (Jinja2 templates) remains as a reference implementation but is now secondary to the Flutter mobile app.

### Key Changes:
- Primary frontend is now Flutter (not included in this repo)
- Web UI serves as admin interface and API documentation
- CORS enabled for cross-origin requests from Flutter

## Environment Variables

### New Variables
```env
# Optional: AI model path
AI_MODEL_PATH=/path/to/model.tflite

# Optional: Central sync server
SYNC_SERVER_URL=https://api.introspect.example.com

# Optional: File upload directory
UPLOAD_DIR=./uploads
```

## Breaking Changes

⚠️ **Important**: This is a complete repurposing, not a backward-compatible update.

1. **Database schema is completely different** - No migration path from todos to test results
2. **All API endpoints have changed** - Existing clients will break
3. **Authentication remains the same** - User tokens are compatible
4. **New dependencies required** - Run `pip install -r requirements.txt`

## Rollback Procedure

If you need to rollback to the todo app:

```bash
# 1. Checkout the previous version
git checkout <previous-commit-hash>

# 2. Restore database backup
cp introspect.db.backup introspect.db

# 3. Reinstall old dependencies
pip install -r requirements.txt

# 4. Restart server
uvicorn src.main:app --reload
```

## Support

For questions about the migration:
1. Review the new README.md
2. Check API_DOCUMENTATION.md for endpoint details
3. See QUICKSTART.md for getting started
4. Open an issue on GitHub

## Summary

This migration transforms a simple todo application into a comprehensive malaria diagnostics system while preserving:
- ✅ Clean architecture principles
- ✅ Authentication system
- ✅ User management
- ✅ Testing infrastructure
- ✅ Docker deployment
- ✅ Code quality and structure

New capabilities added:
- ✅ AI-powered image analysis
- ✅ Patient management
- ✅ Clinic management
- ✅ Surveillance dashboard
- ✅ Offline sync capability
- ✅ File storage system
- ✅ Flutter-ready API

