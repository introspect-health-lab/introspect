from fastapi import APIRouter, status, Query
from typing import List, Optional
from uuid import UUID

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)

@router.post("/", response_model=models.PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(db: DbSession, patient: models.PatientCreate, current_user: CurrentUser):
    """Create a new patient record."""
    return service.create_patient(current_user, db, patient)


@router.get("/", response_model=List[models.PatientResponse])
def get_patients(
    db: DbSession, 
    current_user: CurrentUser,
    clinic_id: Optional[UUID] = Query(None, description="Filter by clinic ID")
):
    """Get all patients, optionally filtered by clinic."""
    return service.get_patients(current_user, db, clinic_id)


@router.get("/search", response_model=List[models.PatientResponse])
def search_patients(
    db: DbSession,
    current_user: CurrentUser,
    q: str = Query(..., description="Search term (name or national ID)"),
    clinic_id: Optional[UUID] = Query(None, description="Filter by clinic ID")
):
    """Search patients by name or national ID."""
    return service.search_patients(current_user, db, q, clinic_id)


@router.get("/{patient_id}", response_model=models.PatientResponse)
def get_patient(db: DbSession, patient_id: UUID, current_user: CurrentUser):
    """Get a patient by ID."""
    return service.get_patient_by_id(current_user, db, patient_id)


@router.put("/{patient_id}", response_model=models.PatientResponse)
def update_patient(db: DbSession, patient_id: UUID, patient_update: models.PatientUpdate, current_user: CurrentUser):
    """Update a patient record."""
    return service.update_patient(current_user, db, patient_id, patient_update)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(db: DbSession, patient_id: UUID, current_user: CurrentUser):
    """Delete a patient record."""
    service.delete_patient(current_user, db, patient_id)

