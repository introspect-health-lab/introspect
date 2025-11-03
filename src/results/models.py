from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.entities.test_result import TestStatus, SyncStatus

class TestResultBase(BaseModel):
    patient_id: UUID
    clinic_id: UUID
    result: TestStatus
    confidence_score: Optional[float] = None
    notes: Optional[str] = None
    symptoms: Optional[str] = None

class TestResultCreate(TestResultBase):
    pass

class TestResultUpdate(BaseModel):
    result: Optional[TestStatus] = None
    notes: Optional[str] = None
    symptoms: Optional[str] = None

class TestResultResponse(TestResultBase):
    id: UUID
    health_worker_id: UUID
    test_date: datetime
    image_path: str
    image_filename: str
    model_version: Optional[str] = None
    processing_time_ms: Optional[float] = None
    sync_status: SyncStatus
    synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class AnalysisRequest(BaseModel):
    """Request model for image analysis."""
    patient_id: UUID
    clinic_id: UUID
    notes: Optional[str] = None
    symptoms: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Response model for image analysis."""
    test_result_id: UUID
    result: TestStatus
    confidence_score: float
    processing_time_ms: float
    message: str

