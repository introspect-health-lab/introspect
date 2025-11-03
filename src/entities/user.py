from sqlalchemy import Column, String, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from ..database.core import Base

class UserRole(enum.Enum):
    HealthWorker = "health_worker"
    Admin = "admin"
    Supervisor = "supervisor"

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.HealthWorker)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=True)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.first_name} {self.last_name}', role='{self.role}')>"