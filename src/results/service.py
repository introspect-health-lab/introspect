from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import UploadFile
from . import models
from src.entities.test_result import TestResult, TestStatus, SyncStatus
from src.auth.models import TokenData
from src.infrastructure.ai_inference import get_inference_service, InferenceResult
from src.infrastructure.file_storage import get_storage_service
from src.exceptions import TestResultNotFoundError, TestResultCreationError
import logging
import tempfile
import os

def create_test_result_from_analysis(
    current_user: TokenData,
    db: Session,
    analysis_request: models.AnalysisRequest,
    image_file: UploadFile,
) -> tuple[TestResult, float, float]:
    """
    Create a test result by analyzing an uploaded image.
    
    Returns:
        Tuple of (test_result, confidence_score, processing_time_ms)
    """
    try:
        # Get services
        inference_service = get_inference_service()
        storage_service = get_storage_service()
        
        # Read file content
        file_content = image_file.file.read()
        
        # Save to temporary file for analysis
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.filename)[1]) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name
        
        try:
            # Validate image
            if not inference_service.validate_image(temp_path):
                raise ValueError("Invalid image file")
            
            # Run AI inference
            inference_result, confidence, processing_time = inference_service.analyze_image(temp_path)
            
            # Map inference result to TestStatus
            result_mapping = {
                InferenceResult.POSITIVE: TestStatus.Positive,
                InferenceResult.NEGATIVE: TestStatus.Negative,
                InferenceResult.INCONCLUSIVE: TestStatus.Inconclusive,
            }
            test_status = result_mapping[inference_result]
            
            # Save image to permanent storage
            image_path, image_filename = storage_service.save_image(
                file_content,
                image_file.filename,
                str(analysis_request.clinic_id)
            )
            
            # Create test result record
            new_result = TestResult(
                patient_id=analysis_request.patient_id,
                clinic_id=analysis_request.clinic_id,
                health_worker_id=current_user.get_uuid(),
                result=test_status,
                confidence_score=confidence,
                image_path=image_path,
                image_filename=image_filename,
                model_version=inference_service.model_version,
                processing_time_ms=processing_time,
                notes=analysis_request.notes,
                symptoms=analysis_request.symptoms,
                sync_status=SyncStatus.Pending,
            )
            
            db.add(new_result)
            db.commit()
            db.refresh(new_result)
            
            logging.info(f"Created test result {new_result.id} with status {test_status.value}")
            return new_result, confidence, processing_time
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logging.error(f"Failed to create test result from analysis. Error: {str(e)}")
        db.rollback()
        raise TestResultCreationError(str(e))


def get_test_results(
    current_user: TokenData,
    db: Session,
    clinic_id: Optional[UUID] = None,
    patient_id: Optional[UUID] = None,
    status: Optional[TestStatus] = None,
) -> List[TestResult]:
    """Get test results with optional filters."""
    query = db.query(TestResult)
    
    if clinic_id:
        query = query.filter(TestResult.clinic_id == clinic_id)
    
    if patient_id:
        query = query.filter(TestResult.patient_id == patient_id)
    
    if status:
        query = query.filter(TestResult.result == status)
    
    results = query.order_by(TestResult.test_date.desc()).all()
    logging.info(f"Retrieved {len(results)} test results")
    return results


def get_test_result_by_id(current_user: TokenData, db: Session, result_id: UUID) -> TestResult:
    """Get a test result by ID."""
    result = db.query(TestResult).filter(TestResult.id == result_id).first()
    if not result:
        logging.warning(f"Test result {result_id} not found")
        raise TestResultNotFoundError(result_id)
    logging.info(f"Retrieved test result {result_id}")
    return result


def update_test_result(
    current_user: TokenData,
    db: Session,
    result_id: UUID,
    result_update: models.TestResultUpdate
) -> TestResult:
    """Update a test result."""
    result = get_test_result_by_id(current_user, db, result_id)
    
    update_data = result_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(result, field, value)
    
    result.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(result)
    logging.info(f"Updated test result {result_id}")
    return result


def mark_as_synced(current_user: TokenData, db: Session, result_id: UUID) -> TestResult:
    """Mark a test result as synced."""
    result = get_test_result_by_id(current_user, db, result_id)
    result.sync_status = SyncStatus.Synced
    result.synced_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(result)
    logging.info(f"Marked test result {result_id} as synced")
    return result


def get_pending_sync_results(current_user: TokenData, db: Session) -> List[TestResult]:
    """Get all test results pending sync."""
    results = db.query(TestResult).filter(
        TestResult.sync_status == SyncStatus.Pending
    ).all()
    logging.info(f"Retrieved {len(results)} pending sync results")
    return results

