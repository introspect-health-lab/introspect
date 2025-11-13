from fastapi import APIRouter, status, Query, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser
from src.entities.test_result import TestStatus

router = APIRouter(
    prefix="/api/results",
    tags=["Test Results"]
)

@router.post("/analyze", response_model=models.AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_image(
    db: DbSession,
    current_user: CurrentUser,
    image: UploadFile = File(..., description="Blood smear image"),
    patient_id: UUID = Form(...),
    clinic_id: UUID = Form(...),
    notes: Optional[str] = Form(None),
    symptoms: Optional[str] = Form(None),
):
    """
    Upload and analyze a blood smear image for malaria detection.
    Returns the analysis result and creates a test result record.
    """
    analysis_request = models.AnalysisRequest(
        patient_id=patient_id,
        clinic_id=clinic_id,
        notes=notes,
        symptoms=symptoms
    )

    test_result, confidence, processing_time = service.create_test_result_from_analysis(
        current_user, db, analysis_request, image
    )

    return models.AnalysisResponse(
        test_result_id=test_result.id,
        result=test_result.result,
        confidence_score=confidence,
        processing_time_ms=processing_time,
        message=f"Analysis complete: {test_result.result.value}"
    )


@router.post("/capture-and-analyze", response_model=models.AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def capture_and_analyze(
    db: DbSession,
    current_user: CurrentUser,
    patient_id: UUID = Form(...),
    clinic_id: UUID = Form(...),
    notes: Optional[str] = Form(None),
    symptoms: Optional[str] = Form(None),
):
    """
    Capture an image from Raspberry Pi camera and analyze for malaria detection.
    This endpoint is designed for edge AI deployment on Raspberry Pi 5 with Camera Module 3.
    Returns the analysis result and creates a test result record.
    """
    analysis_request = models.AnalysisRequest(
        patient_id=patient_id,
        clinic_id=clinic_id,
        notes=notes,
        symptoms=symptoms
    )

    test_result, confidence, processing_time = service.create_test_result_from_camera_capture(
        current_user, db, analysis_request
    )

    return models.AnalysisResponse(
        test_result_id=test_result.id,
        result=test_result.result,
        confidence_score=confidence,
        processing_time_ms=processing_time,
        message=f"Analysis complete: {test_result.result.value}"
    )


@router.get("/", response_model=List[models.TestResultResponse])
def get_test_results(
    db: DbSession,
    current_user: CurrentUser,
    clinic_id: Optional[UUID] = Query(None, description="Filter by clinic ID"),
    patient_id: Optional[UUID] = Query(None, description="Filter by patient ID"),
    status: Optional[TestStatus] = Query(None, description="Filter by test status"),
):
    """Get test results with optional filters."""
    return service.get_test_results(current_user, db, clinic_id, patient_id, status)


@router.get("/pending-sync", response_model=List[models.TestResultResponse])
def get_pending_sync_results(db: DbSession, current_user: CurrentUser):
    """Get all test results pending synchronization."""
    return service.get_pending_sync_results(current_user, db)


@router.get("/{result_id}", response_model=models.TestResultResponse)
def get_test_result(db: DbSession, result_id: UUID, current_user: CurrentUser):
    """Get a test result by ID."""
    return service.get_test_result_by_id(current_user, db, result_id)


@router.put("/{result_id}", response_model=models.TestResultResponse)
def update_test_result(
    db: DbSession,
    result_id: UUID,
    result_update: models.TestResultUpdate,
    current_user: CurrentUser
):
    """Update a test result."""
    return service.update_test_result(current_user, db, result_id, result_update)


@router.post("/{result_id}/sync", response_model=models.TestResultResponse)
def mark_as_synced(db: DbSession, result_id: UUID, current_user: CurrentUser):
    """Mark a test result as synced."""
    return service.mark_as_synced(current_user, db, result_id)

