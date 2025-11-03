from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from . import models
from src.entities.patient import Patient
from src.auth.models import TokenData
from src.exceptions import PatientNotFoundError, PatientCreationError
import logging

def create_patient(current_user: TokenData, db: Session, patient: models.PatientCreate) -> Patient:
    """Create a new patient record."""
    try:
        new_patient = Patient(**patient.model_dump())
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        logging.info(f"Created new patient {new_patient.id} by user {current_user.get_uuid()}")
        return new_patient
    except Exception as e:
        logging.error(f"Failed to create patient. Error: {str(e)}")
        db.rollback()
        raise PatientCreationError(str(e))


def get_patients(current_user: TokenData, db: Session, clinic_id: Optional[UUID] = None) -> List[Patient]:
    """Get all patients, optionally filtered by clinic."""
    query = db.query(Patient)
    
    if clinic_id:
        query = query.filter(Patient.clinic_id == clinic_id)
    
    patients = query.all()
    logging.info(f"Retrieved {len(patients)} patients for user {current_user.get_uuid()}")
    return patients


def get_patient_by_id(current_user: TokenData, db: Session, patient_id: UUID) -> Patient:
    """Get a patient by ID."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        logging.warning(f"Patient {patient_id} not found")
        raise PatientNotFoundError(patient_id)
    logging.info(f"Retrieved patient {patient_id}")
    return patient


def search_patients(current_user: TokenData, db: Session, search_term: str, clinic_id: Optional[UUID] = None) -> List[Patient]:
    """Search patients by name or national ID."""
    query = db.query(Patient).filter(
        or_(
            Patient.first_name.ilike(f"%{search_term}%"),
            Patient.last_name.ilike(f"%{search_term}%"),
            Patient.national_id.ilike(f"%{search_term}%")
        )
    )
    
    if clinic_id:
        query = query.filter(Patient.clinic_id == clinic_id)
    
    patients = query.all()
    logging.info(f"Search for '{search_term}' returned {len(patients)} patients")
    return patients


def update_patient(current_user: TokenData, db: Session, patient_id: UUID, patient_update: models.PatientUpdate) -> Patient:
    """Update a patient record."""
    patient = get_patient_by_id(current_user, db, patient_id)
    
    update_data = patient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    logging.info(f"Updated patient {patient_id} by user {current_user.get_uuid()}")
    return patient


def delete_patient(current_user: TokenData, db: Session, patient_id: UUID) -> None:
    """Delete a patient record."""
    patient = get_patient_by_id(current_user, db, patient_id)
    db.delete(patient)
    db.commit()
    logging.info(f"Deleted patient {patient_id} by user {current_user.get_uuid()}")

