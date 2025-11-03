"""
File Storage Service for blood smear images
"""

import os
import uuid
from pathlib import Path
from typing import Tuple
import shutil
import logging
from datetime import datetime

class FileStorageService:
    """Service for storing and managing blood smear images."""
    
    def __init__(self, base_path: str = "./uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"File storage initialized at: {self.base_path}")
    
    def save_image(self, file_content: bytes, original_filename: str, clinic_id: str) -> Tuple[str, str]:
        """
        Save an uploaded image file.
        
        Args:
            file_content: Binary content of the file
            original_filename: Original filename from upload
            clinic_id: ID of the clinic for organization
            
        Returns:
            Tuple of (file_path, stored_filename)
        """
        # Create directory structure: uploads/clinic_id/YYYY-MM/
        date_path = datetime.now().strftime("%Y-%m")
        clinic_dir = self.base_path / str(clinic_id) / date_path
        clinic_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(original_filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = clinic_dir / unique_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        logging.info(f"Image saved: {file_path}")
        
        # Return relative path from base
        relative_path = str(file_path.relative_to(self.base_path))
        return relative_path, unique_filename
    
    def get_image_path(self, relative_path: str) -> Path:
        """
        Get the full path to an image.
        
        Args:
            relative_path: Relative path from base storage
            
        Returns:
            Full Path object
        """
        return self.base_path / relative_path
    
    def delete_image(self, relative_path: str) -> bool:
        """
        Delete an image file.
        
        Args:
            relative_path: Relative path from base storage
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            file_path = self.get_image_path(relative_path)
            if file_path.exists():
                file_path.unlink()
                logging.info(f"Image deleted: {file_path}")
                return True
            else:
                logging.warning(f"Image not found for deletion: {file_path}")
                return False
        except Exception as e:
            logging.error(f"Error deleting image: {str(e)}")
            return False
    
    def get_storage_stats(self) -> dict:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with storage stats
        """
        total_size = 0
        file_count = 0
        
        for file_path in self.base_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "total_files": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "base_path": str(self.base_path)
        }


# Singleton instance
_storage_service = None

def get_storage_service() -> FileStorageService:
    """Get or create the singleton storage service instance."""
    global _storage_service
    if _storage_service is None:
        _storage_service = FileStorageService()
    return _storage_service

