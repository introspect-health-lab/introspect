"""
Sync Service for offline-first capability
Handles synchronization of test results when connection is available
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict
from src.entities.test_result import TestResult, SyncStatus
import logging

class SyncService:
    """
    Service for synchronizing offline test results.
    In a production environment, this would sync with a central server.
    """
    
    def __init__(self, central_server_url: str = None):
        self.central_server_url = central_server_url or "https://api.introspect.example.com"
        logging.info(f"Sync service initialized with server: {self.central_server_url}")
    
    def get_pending_results(self, db: Session) -> List[TestResult]:
        """Get all test results pending synchronization."""
        pending = db.query(TestResult).filter(
            TestResult.sync_status == SyncStatus.Pending
        ).all()
        logging.info(f"Found {len(pending)} results pending sync")
        return pending
    
    def sync_result(self, db: Session, result: TestResult) -> bool:
        """
        Sync a single test result to the central server.
        
        Args:
            db: Database session
            result: TestResult to sync
            
        Returns:
            True if sync successful, False otherwise
        """
        try:
            # PLACEHOLDER: In production, this would make an HTTP request to central server
            # Example:
            # import requests
            # response = requests.post(
            #     f"{self.central_server_url}/api/sync/results",
            #     json={
            #         "id": str(result.id),
            #         "patient_id": str(result.patient_id),
            #         "clinic_id": str(result.clinic_id),
            #         "result": result.result.value,
            #         "confidence_score": result.confidence_score,
            #         "test_date": result.test_date.isoformat(),
            #         # ... other fields
            #     },
            #     headers={"Authorization": f"Bearer {api_token}"}
            # )
            # if response.status_code != 200:
            #     raise Exception(f"Sync failed: {response.text}")
            
            # Simulate successful sync
            result.sync_status = SyncStatus.Synced
            result.synced_at = datetime.now(timezone.utc)
            db.commit()
            
            logging.info(f"Successfully synced result {result.id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to sync result {result.id}: {str(e)}")
            result.sync_status = SyncStatus.Failed
            db.commit()
            return False
    
    def sync_all_pending(self, db: Session) -> Dict[str, int]:
        """
        Sync all pending test results.
        
        Returns:
            Dictionary with sync statistics
        """
        pending_results = self.get_pending_results(db)
        
        stats = {
            "total": len(pending_results),
            "synced": 0,
            "failed": 0
        }
        
        for result in pending_results:
            if self.sync_result(db, result):
                stats["synced"] += 1
            else:
                stats["failed"] += 1
        
        logging.info(f"Sync complete: {stats['synced']} synced, {stats['failed']} failed out of {stats['total']}")
        return stats
    
    def retry_failed_syncs(self, db: Session) -> Dict[str, int]:
        """
        Retry synchronization for previously failed results.
        
        Returns:
            Dictionary with retry statistics
        """
        failed_results = db.query(TestResult).filter(
            TestResult.sync_status == SyncStatus.Failed
        ).all()
        
        stats = {
            "total": len(failed_results),
            "synced": 0,
            "still_failed": 0
        }
        
        for result in failed_results:
            # Reset to pending before retry
            result.sync_status = SyncStatus.Pending
            db.commit()
            
            if self.sync_result(db, result):
                stats["synced"] += 1
            else:
                stats["still_failed"] += 1
        
        logging.info(f"Retry complete: {stats['synced']} synced, {stats['still_failed']} still failed")
        return stats
    
    def get_sync_status(self, db: Session) -> Dict[str, int]:
        """
        Get overall sync status statistics.
        
        Returns:
            Dictionary with sync status counts
        """
        total = db.query(TestResult).count()
        pending = db.query(TestResult).filter(TestResult.sync_status == SyncStatus.Pending).count()
        synced = db.query(TestResult).filter(TestResult.sync_status == SyncStatus.Synced).count()
        failed = db.query(TestResult).filter(TestResult.sync_status == SyncStatus.Failed).count()
        
        return {
            "total_results": total,
            "pending": pending,
            "synced": synced,
            "failed": failed,
            "sync_percentage": round((synced / total * 100) if total > 0 else 0, 2)
        }


# Singleton instance
_sync_service = None

def get_sync_service() -> SyncService:
    """Get or create the singleton sync service instance."""
    global _sync_service
    if _sync_service is None:
        _sync_service = SyncService()
    return _sync_service

