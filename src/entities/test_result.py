from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from datetime import datetime, timezone
from ..database.core import Base 

class TestStatus(enum.Enum):
    Positive = "positive"
    Negative = "negative"
    Inconclusive = "inconclusive"

class SyncStatus(enum.Enum):
    Pending = "pending"
    Synced = "synced"
    Failed = "failed"

class TestResult(Base):
    __tablename__ = 'test_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=False)
    health_worker_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Test information
    test_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    result = Column(Enum(TestStatus), nullable=False)
    confidence_score = Column(Float, nullable=True)  # AI model confidence (0-1)
    
    # Image information
    image_path = Column(String, nullable=False)  # Path to stored blood smear image
    image_filename = Column(String, nullable=False)
    
    # AI analysis metadata
    model_version = Column(String, nullable=True)
    processing_time_ms = Column(Float, nullable=True)
    
    # Additional notes
    notes = Column(Text, nullable=True)
    symptoms = Column(String, nullable=True)  # Comma-separated symptoms
    
    # Sync status for offline capability
    sync_status = Column(Enum(SyncStatus), nullable=False, default=SyncStatus.Pending)
    synced_at = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TestResult(patient_id='{self.patient_id}', result='{self.result}', confidence={self.confidence_score})>"

