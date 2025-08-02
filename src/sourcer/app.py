"""Main application entry point for Sourcer MVP."""

import sys
import logging
from typing import Optional

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from sourcer.ui.main_window import MainWindow
from sourcer.utils.config_loader import ConfigLoader
from sourcer.core.orchestrator import Orchestrator


class SourcerApp:
    """Main application class for Sourcer MVP."""

    def __init__(self) -> None:
        """Initialize the Sourcer application."""
        self.app: Optional[QApplication] = None
        self.main_window: Optional[MainWindow] = None
        self.config: Optional[ConfigLoader] = None
        self.orchestrator: Optional[Orchestrator] = None
        self.logger = logging.getLogger(__name__)

    def initialize(self) -> None:
        """Initialize application components."""
        # Load configuration
        self.config = ConfigLoader()
        
        # Set up logging
        self._setup_logging()
        
        # Create Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(self.config.get("Application", "name"))
        self.app.setOrganizationName("Sourcer")
        
        # Enable high DPI scaling
        self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Initialize orchestrator
        self.orchestrator = Orchestrator(self.config)
        
        # Create main window
        self.main_window = MainWindow(self.orchestrator, self.config)
        
        self.logger.info("Sourcer application initialized successfully")

    def _setup_logging(self) -> None:
        """Configure application logging."""
        log_level = self.config.get("Logging", "level", fallback="INFO")
        log_file = self.config.get("Logging", "file", fallback="sourcer.log")
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def run(self) -> int:
        """Run the application."""
        if not self.app or not self.main_window:
            raise RuntimeError("Application not initialized")
        
        self.main_window.show()
        self.logger.info("Starting Sourcer application")
        
        return self.app.exec()

    def cleanup(self) -> None:
        """Clean up application resources."""
        if self.orchestrator:
            self.orchestrator.cleanup()
        
        self.logger.info("Sourcer application shut down")


def create_app() -> SourcerApp:
    """Create and return a Sourcer application instance."""
    app = SourcerApp()
    app.initialize()
    return app