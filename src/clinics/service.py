from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models
from src.entities.clinic import Clinic
from src.auth.models import TokenData
from src.exceptions import ClinicNotFoundError, ClinicCreationError
import logging

def create_clinic(current_user: TokenData, db: Session, clinic: models.ClinicCreate) -> Clinic:
    """Create a new clinic."""
    try:
        new_clinic = Clinic(**clinic.model_dump())
        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)
        logging.info(f"Created new clinic {new_clinic.id} by user {current_user.get_uuid()}")
        return new_clinic
    except Exception as e:
        logging.error(f"Failed to create clinic. Error: {str(e)}")
        db.rollback()
        raise ClinicCreationError(str(e))


def get_clinics(current_user: TokenData, db: Session, district: Optional[str] = None) -> List[Clinic]:
    """Get all clinics, optionally filtered by district."""
    query = db.query(Clinic)
    
    if district:
        query = query.filter(Clinic.district == district)
    
    clinics = query.all()
    logging.info(f"Retrieved {len(clinics)} clinics")
    return clinics


def get_clinic_by_id(current_user: TokenData, db: Session, clinic_id: UUID) -> Clinic:
    """Get a clinic by ID."""
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        logging.warning(f"Clinic {clinic_id} not found")
        raise ClinicNotFoundError(clinic_id)
    logging.info(f"Retrieved clinic {clinic_id}")
    return clinic


def update_clinic(current_user: TokenData, db: Session, clinic_id: UUID, clinic_update: models.ClinicUpdate) -> Clinic:
    """Update a clinic."""
    clinic = get_clinic_by_id(current_user, db, clinic_id)
    
    update_data = clinic_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(clinic, field, value)
    
    db.commit()
    db.refresh(clinic)
    logging.info(f"Updated clinic {clinic_id}")
    return clinic


def delete_clinic(current_user: TokenData, db: Session, clinic_id: UUID) -> None:
    """Delete a clinic."""
    clinic = get_clinic_by_id(current_user, db, clinic_id)
    db.delete(clinic)
    db.commit()
    logging.info(f"Deleted clinic {clinic_id}")

