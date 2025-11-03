from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from ..database.core import DbSession
from ..auth.service import CurrentUser
from ..infrastructure.sync_service import get_sync_service

router = APIRouter(
    prefix="/api/sync",
    tags=["Sync"]
)

class SyncStats(BaseModel):
    """Sync statistics response model."""
    total: int
    synced: int
    failed: int

class SyncStatusResponse(BaseModel):
    """Overall sync status response."""
    total_results: int
    pending: int
    synced: int
    failed: int
    sync_percentage: float

@router.post("/all", response_model=SyncStats)
def sync_all_pending(db: DbSession, current_user: CurrentUser, background_tasks: BackgroundTasks):
    """
    Sync all pending test results to the central server.
    This operation runs in the background.
    """
    sync_service = get_sync_service()
    
    # Run sync in background
    def sync_task():
        stats = sync_service.sync_all_pending(db)
        return stats
    
    # For now, run synchronously (in production, use background_tasks.add_task)
    stats = sync_task()
    return SyncStats(**stats)


@router.post("/retry", response_model=SyncStats)
def retry_failed_syncs(db: DbSession, current_user: CurrentUser):
    """Retry synchronization for previously failed results."""
    sync_service = get_sync_service()
    stats = sync_service.retry_failed_syncs(db)
    return SyncStats(**stats)


@router.get("/status", response_model=SyncStatusResponse)
def get_sync_status(db: DbSession, current_user: CurrentUser):
    """Get overall sync status statistics."""
    sync_service = get_sync_service()
    status = sync_service.get_sync_status(db)
    return SyncStatusResponse(**status)

