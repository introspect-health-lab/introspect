from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ClinicBase(BaseModel):
    name: str
    district: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

class ClinicResponse(ClinicBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

