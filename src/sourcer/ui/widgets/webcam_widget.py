"""Webcam display widget."""

import logging
from typing import Optional

import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

from sourcer.utils.config_loader import ConfigLoader


class WebcamWidget(QWidget):
    """Widget for displaying webcam feed."""
    
    # Signals
    frame_updated = pyqtSignal(np.ndarray)
    
    def __init__(self, config: ConfigLoader, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the webcam widget.
        
        Args:
            config: Configuration loader instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get configuration
        self.width = self.config.get_int("UI", "webcam_width", 640)
        self.height = self.config.get_int("UI", "webcam_height", 480)
        self.fps = self.config.get_int("UI", "webcam_fps", 30)
        
        # Video capture
        self.capture: Optional[cv2.VideoCapture] = None
        self.current_frame: Optional[np.ndarray] = None
        self.is_active = False
        
        # Initialize UI
        self._init_ui()
        
        # Start capture
        self.start_capture()

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setMinimumSize(self.width, self.height)
        
        # Set placeholder text
        self.video_label.setText("Initializing webcam...")
        self.video_label.setStyleSheet(
            "background-color: black; color: white; font-size: 16px;"
        )
        
        layout.addWidget(self.video_label)
        
        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

    def start_capture(self) -> bool:
        """
        Start webcam capture.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Try different camera indices
            for index in [0, 1, -1]:
                self.capture = cv2.VideoCapture(index)
                if self.capture.isOpened():
                    # Set capture properties
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self.capture.set(cv2.CAP_PROP_FPS, self.fps)
                    
                    self.is_active = True
                    self.timer.start(int(1000 / self.fps))  # Update interval in ms
                    
                    self.logger.info(f"Webcam started on index {index}")
                    return True
            
            # No camera found
            self.logger.warning("No webcam found")
            self._show_error("No webcam detected")
            return False
            
        except Exception as e:
            self.logger.error(f"Error starting webcam: {e}")
            self._show_error(f"Camera error: {str(e)}")
            return False

    def stop_capture(self) -> None:
        """Stop webcam capture."""
        self.is_active = False
        self.timer.stop()
        
        if self.capture:
            self.capture.release()
            self.capture = None
        
        self.logger.info("Webcam stopped")

    def _update_frame(self) -> None:
        """Update the displayed frame."""
        if not self.capture or not self.is_active:
            return
        
        ret, frame = self.capture.read()
        if ret:
            # Store current frame
            self.current_frame = frame.copy()
            
            # Convert to RGB (OpenCV uses BGR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Emit signal
            self.frame_updated.emit(rgb_frame)
            
            # Convert to Qt format and display
            self._display_frame(rgb_frame)
        else:
            self.logger.warning("Failed to read frame from webcam")

    def _display_frame(self, frame: np.ndarray) -> None:
        """
        Display a frame in the widget.
        
        Args:
            frame: RGB frame to display
        """
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        
        # Create QImage
        q_image = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )
        
        # Scale to fit widget while maintaining aspect ratio
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.video_label.setPixmap(scaled_pixmap)

    def _show_error(self, message: str) -> None:
        """
        Show error message in the widget.
        
        Args:
            message: Error message to display
        """
        self.video_label.setText(message)
        self.video_label.setStyleSheet(
            "background-color: black; color: red; font-size: 16px;"
        )

    def get_current_frame(self) -> Optional[np.ndarray]:
        """
        Get the current frame.
        
        Returns:
            Current frame as numpy array or None
        """
        return self.current_frame.copy() if self.current_frame is not None else None

    def resizeEvent(self, event) -> None:
        """Handle widget resize event."""
        super().resizeEvent(event)
        # Update display if we have a current frame
        if self.current_frame is not None:
            rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            self._display_frame(rgb_frame)

    def closeEvent(self, event) -> None:
        """Handle widget close event."""
        self.stop_capture()
        super().closeEvent(event)