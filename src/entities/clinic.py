from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 

class Clinic(Base):
    __tablename__ = 'clinics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    region = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)

    def __repr__(self):
        return f"<Clinic(name='{self.name}', district='{self.district}', region='{self.region}')>"

