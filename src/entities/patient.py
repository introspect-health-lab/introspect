from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from ..database.core import Base 

class Gender(enum.Enum):
    Male = "male"
    Female = "female"
    Other = "other"

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=False)
    phone_number = Column(String, nullable=True)
    national_id = Column(String, nullable=True, unique=True)
    village = Column(String, nullable=True)
    district = Column(String, nullable=True)

    def __repr__(self):
        return f"<Patient(name='{self.first_name} {self.last_name}', id='{self.national_id}')>"

