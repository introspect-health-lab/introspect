from fastapi import APIRouter, status, Query
from typing import List, Optional
from uuid import UUID

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/api/clinics",
    tags=["Clinics"]
)

@router.post("/", response_model=models.ClinicResponse, status_code=status.HTTP_201_CREATED)
def create_clinic(db: DbSession, clinic: models.ClinicCreate, current_user: CurrentUser):
    """Create a new clinic."""
    return service.create_clinic(current_user, db, clinic)


@router.get("/", response_model=List[models.ClinicResponse])
def get_clinics(
    db: DbSession,
    current_user: CurrentUser,
    district: Optional[str] = Query(None, description="Filter by district")
):
    """Get all clinics, optionally filtered by district."""
    return service.get_clinics(current_user, db, district)


@router.get("/{clinic_id}", response_model=models.ClinicResponse)
def get_clinic(db: DbSession, clinic_id: UUID, current_user: CurrentUser):
    """Get a clinic by ID."""
    return service.get_clinic_by_id(current_user, db, clinic_id)


@router.put("/{clinic_id}", response_model=models.ClinicResponse)
def update_clinic(db: DbSession, clinic_id: UUID, clinic_update: models.ClinicUpdate, current_user: CurrentUser):
    """Update a clinic."""
    return service.update_clinic(current_user, db, clinic_id, clinic_update)


@router.delete("/{clinic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinic(db: DbSession, clinic_id: UUID, current_user: CurrentUser):
    """Delete a clinic."""
    service.delete_clinic(current_user, db, clinic_id)

