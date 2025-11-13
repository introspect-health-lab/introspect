"""
Camera Service for Raspberry Pi Camera Module 3
Handles image capture from the Raspberry Pi camera for malaria diagnostics.
"""

import logging
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

class CameraService:
    """
    Service for capturing images from Raspberry Pi Camera Module 3.
    Falls back to mock mode if camera is not available (for development).
    """
    
    def __init__(self):
        self.camera = None
        self.is_available = False
        self.use_mock = False
        
        # Camera configuration
        self.resolution = (2304, 1296)  # Camera Module 3 default resolution
        self.format = "jpeg"
        
        logging.info("Initializing Camera Service for Raspberry Pi Camera Module 3")
        self._initialize_camera()
    
    def _initialize_camera(self):
        """
        Initialize the Raspberry Pi camera.
        Falls back to mock mode if camera is not available.
        """
        try:
            # Try to import picamera2
            from picamera2 import Picamera2
            
            # Initialize camera
            self.camera = Picamera2()
            
            # Configure camera for still capture
            config = self.camera.create_still_configuration(
                main={"size": self.resolution, "format": "RGB888"}
            )
            self.camera.configure(config)
            
            self.is_available = True
            self.use_mock = False
            logging.info(f"Camera initialized successfully with resolution {self.resolution}")
            
        except ImportError:
            logging.warning("picamera2 not installed. Using mock mode. Install with: pip install picamera2")
            self.use_mock = True
            self.is_available = False
        except Exception as e:
            logging.warning(f"Camera not available: {str(e)}. Using mock mode.")
            self.use_mock = True
            self.is_available = False
    
    def capture_image(self, output_path: Optional[str] = None) -> str:
        """
        Capture an image from the camera.
        
        Args:
            output_path: Optional path to save the image. If None, uses temp file.
            
        Returns:
            Path to the captured image file
        """
        if self.use_mock:
            return self._capture_mock_image(output_path)
        
        try:
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"camera_capture_{timestamp}.jpg")
            
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Start camera if not already started
            if not self.camera.started:
                self.camera.start()
            
            # Capture image
            self.camera.capture_file(output_path)
            
            logging.info(f"Image captured successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logging.error(f"Error capturing image: {str(e)}")
            raise
    
    def _capture_mock_image(self, output_path: Optional[str] = None) -> str:
        """
        Create a mock image for testing when camera is not available.
        
        Args:
            output_path: Optional path to save the image
            
        Returns:
            Path to the mock image file
        """
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"mock_capture_{timestamp}.jpg")
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create a mock blood smear image
        img = Image.new('RGB', self.resolution, color=(240, 220, 220))
        draw = ImageDraw.Draw(img)
        
        # Draw some random circles to simulate cells
        for _ in range(50):
            x = random.randint(0, self.resolution[0])
            y = random.randint(0, self.resolution[1])
            r = random.randint(20, 50)
            color = (random.randint(200, 255), random.randint(180, 220), random.randint(180, 220))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline=(150, 150, 150))
        
        # Add text overlay
        try:
            draw.text((50, 50), "MOCK CAMERA IMAGE", fill=(255, 0, 0))
        except:
            pass
        
        # Save image
        img.save(output_path, "JPEG", quality=95)
        
        logging.info(f"Mock image created: {output_path}")
        return output_path
    
    def close(self):
        """Close the camera and release resources."""
        if self.camera and not self.use_mock:
            try:
                if self.camera.started:
                    self.camera.stop()
                self.camera.close()
                logging.info("Camera closed successfully")
            except Exception as e:
                logging.error(f"Error closing camera: {str(e)}")


# Singleton instance
_camera_service = None

def get_camera_service() -> CameraService:
    """Get or create the singleton camera service instance."""
    global _camera_service
    if _camera_service is None:
        _camera_service = CameraService()
    return _camera_service

