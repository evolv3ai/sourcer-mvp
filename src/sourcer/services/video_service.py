"""Video capture and management service."""

import logging
import threading
from typing import Optional

import cv2
import numpy as np

from sourcer.utils.config_loader import ConfigLoader


class VideoService:
    """Service for managing video capture from webcam."""

    def __init__(self, config: ConfigLoader) -> None:
        """
        Initialize the video service.
        
        Args:
            config: Configuration loader instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get configuration
        self.width = self.config.get_int("UI", "webcam_width", 640)
        self.height = self.config.get_int("UI", "webcam_height", 480)
        self.fps = self.config.get_int("UI", "webcam_fps", 30)
        
        # Video capture
        self.capture: Optional[cv2.VideoCapture] = None
        self.current_frame: Optional[np.ndarray] = None
        self.is_running = False
        
        # Threading
        self.capture_thread: Optional[threading.Thread] = None
        self.frame_lock = threading.Lock()

    def start(self) -> bool:
        """
        Start video capture.
        
        Returns:
            True if successful, False otherwise
        """
        if self.is_running:
            self.logger.warning("Video service already running")
            return True
        
        # Initialize capture
        if not self._initialize_capture():
            return False
        
        # Start capture thread
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        self.logger.info("Video service started")
        return True

    def stop(self) -> None:
        """Stop video capture."""
        self.is_running = False
        
        # Wait for thread to finish
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
        
        # Release capture
        if self.capture:
            self.capture.release()
            self.capture = None
        
        self.logger.info("Video service stopped")

    def _initialize_capture(self) -> bool:
        """
        Initialize video capture device.
        
        Returns:
            True if successful, False otherwise
        """
        # Check for mock camera mode (for testing)
        if self.config.get_bool("Development", "MOCK_CAMERA", False):
            self.logger.info("Using mock camera mode")
            return True
        
        # Try different camera indices
        for index in [0, 1, -1]:
            try:
                self.capture = cv2.VideoCapture(index)
                if self.capture.isOpened():
                    # Set capture properties
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self.capture.set(cv2.CAP_PROP_FPS, self.fps)
                    
                    # Test read
                    ret, _ = self.capture.read()
                    if ret:
                        self.logger.info(f"Camera initialized on index {index}")
                        return True
                    else:
                        self.capture.release()
            except Exception as e:
                self.logger.error(f"Error initializing camera {index}: {e}")
        
        self.logger.error("No working camera found")
        return False

    def _capture_loop(self) -> None:
        """Main capture loop running in separate thread."""
        while self.is_running:
            if self.capture and self.capture.isOpened():
                ret, frame = self.capture.read()
                if ret:
                    with self.frame_lock:
                        self.current_frame = frame.copy()
                else:
                    self.logger.warning("Failed to read frame")
            elif self.config.get_bool("Development", "MOCK_CAMERA", False):
                # Generate mock frame
                with self.frame_lock:
                    self.current_frame = self._generate_mock_frame()
            
            # Small delay to control frame rate
            threading.Event().wait(1.0 / self.fps)

    def _generate_mock_frame(self) -> np.ndarray:
        """
        Generate a mock frame for testing.
        
        Returns:
            Mock frame as numpy array
        """
        # Create a simple test pattern
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Add some color gradients
        for y in range(self.height):
            for x in range(self.width):
                frame[y, x] = [
                    int(255 * x / self.width),  # Red gradient
                    int(255 * y / self.height),  # Green gradient
                    128  # Constant blue
                ]
        
        # Add timestamp text
        timestamp = threading.current_thread().name
        cv2.putText(
            frame,
            f"Mock Camera - {timestamp}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        return frame

    def get_current_frame(self) -> Optional[np.ndarray]:
        """
        Get the current captured frame.
        
        Returns:
            Current frame as numpy array or None
        """
        with self.frame_lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None

    def save_frame(self, filepath: str) -> bool:
        """
        Save current frame to file.
        
        Args:
            filepath: Path to save the frame
            
        Returns:
            True if successful, False otherwise
        """
        frame = self.get_current_frame()
        if frame is not None:
            try:
                cv2.imwrite(filepath, frame)
                self.logger.info(f"Frame saved to {filepath}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to save frame: {e}")
        return False

    def get_info(self) -> dict:
        """
        Get video capture information.
        
        Returns:
            Dictionary with capture info
        """
        info = {
            "is_running": self.is_running,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "has_frame": self.current_frame is not None
        }
        
        if self.capture and self.capture.isOpened():
            info.update({
                "actual_width": int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "actual_height": int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "actual_fps": self.capture.get(cv2.CAP_PROP_FPS)
            })
        
        return info