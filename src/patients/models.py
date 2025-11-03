from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.entities.patient import Gender

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    gender: Gender
    phone_number: Optional[str] = None
    national_id: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None

class PatientCreate(PatientBase):
    clinic_id: UUID

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None
    national_id: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None

class PatientResponse(PatientBase):
    id: UUID
    clinic_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

