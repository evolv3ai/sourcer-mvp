"""Main application window."""

import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QSplitter,
    QMenuBar, QMenu, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction, QKeySequence

from sourcer.ui.widgets.webcam_widget import WebcamWidget
from sourcer.ui.widgets.chat_widget import ChatWidget
from sourcer.core.orchestrator import Orchestrator
from sourcer.utils.config_loader import ConfigLoader


class MainWindow(QMainWindow):
    """Main application window for Sourcer MVP."""

    # Signals
    text_input_submitted = pyqtSignal(str)
    voice_input_toggled = pyqtSignal()

    def __init__(self, orchestrator: Orchestrator, config: ConfigLoader) -> None:
        """
        Initialize the main window.
        
        Args:
            orchestrator: Core orchestrator instance
            config: Configuration loader instance
        """
        super().__init__()
        self.orchestrator = orchestrator
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._displayed_history: list = []  # Track displayed messages
        
        # Initialize UI
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()
        self._connect_signals()
        
        # Start services
        self.orchestrator.start_services()
        
        # Start update timer
        self._start_timers()
        
        self.logger.info("Main window initialized")

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle(self.config.get("UI", "window_title"))
        self.resize(
            self.config.get_int("UI", "window_width", 1200),
            self.config.get_int("UI", "window_height", 800)
        )
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left pane - Webcam feed
        left_pane = QWidget()
        left_layout = QVBoxLayout(left_pane)
        
        # Webcam widget
        self.webcam_widget = WebcamWidget(self.config)
        left_layout.addWidget(self.webcam_widget)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.voice_button = QPushButton("🎤 Start Voice Input")
        self.voice_button.setCheckable(True)
        self.voice_button.setToolTip("Toggle voice input (or press Space)")
        controls_layout.addWidget(self.voice_button)
        
        self.analyze_button = QPushButton("📸 Analyze Now")
        self.analyze_button.setToolTip("Analyze current frame")
        controls_layout.addWidget(self.analyze_button)
        
        left_layout.addLayout(controls_layout)
        
        # Right pane - Chat interface
        right_pane = QWidget()
        right_layout = QVBoxLayout(right_pane)
        
        # Chat widget
        self.chat_widget = ChatWidget(self.config)
        right_layout.addWidget(self.chat_widget)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your question here...")
        self.text_input.returnPressed.connect(self._on_text_input_submitted)
        input_layout.addWidget(self.text_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self._on_text_input_submitted)
        input_layout.addWidget(self.send_button)
        
        right_layout.addLayout(input_layout)
        
        # Add panes to splitter
        splitter.addWidget(left_pane)
        splitter.addWidget(right_pane)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        clear_action = QAction("&Clear History", self)
        clear_action.setShortcut(QKeySequence("Ctrl+L"))
        clear_action.triggered.connect(self._on_clear_history)
        edit_menu.addAction(clear_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence.StandardKey.FullScreen)
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        repeat_action = QAction("&Repeat Last Response", self)
        repeat_action.setShortcut(QKeySequence("Ctrl+R"))
        repeat_action.triggered.connect(self._on_repeat_last)
        tools_menu.addAction(repeat_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets
        self.status_label = QWidget()
        self.status_bar.addPermanentWidget(self.status_label)
        
        self.status_bar.showMessage("Ready")

    def _connect_signals(self) -> None:
        """Connect UI signals to handlers."""
        # Voice button
        self.voice_button.toggled.connect(self._on_voice_toggle)
        
        # Analyze button
        self.analyze_button.clicked.connect(self._on_analyze_clicked)
        
        # Connect to orchestrator
        self.text_input_submitted.connect(self.orchestrator.process_text_input)

    def _start_timers(self) -> None:
        """Start update timers."""
        # Voice input timer
        self.voice_timer = QTimer()
        self.voice_timer.timeout.connect(self._check_voice_input)
        self.voice_timer.start(100)  # Check every 100ms
        
        # UI update timer
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self._update_ui)
        self.ui_timer.start(1000)  # Update every second

    @pyqtSlot()
    def _on_text_input_submitted(self) -> None:
        """Handle text input submission."""
        text = self.text_input.text().strip()
        if not text:
            return
        
        # Clear input
        self.text_input.clear()
        
        # Add to chat
        self.chat_widget.add_message("You", text, "user")
        
        # Process input
        self.text_input_submitted.emit(text)
        
        # Get response and display
        self._process_and_display_response()

    @pyqtSlot(bool)
    def _on_voice_toggle(self, checked: bool) -> None:
        """Handle voice input toggle."""
        is_listening = self.orchestrator.toggle_listening()
        
        if is_listening:
            self.voice_button.setText("🔴 Stop Voice Input")
            self.status_bar.showMessage("Listening...")
        else:
            self.voice_button.setText("🎤 Start Voice Input")
            self.status_bar.showMessage("Ready")

    @pyqtSlot()
    def _on_analyze_clicked(self) -> None:
        """Handle analyze button click."""
        self.status_bar.showMessage("Analyzing...")
        
        # Analyze current frame
        result = self.orchestrator.analyze_current_frame()
        
        if result:
            response = self.orchestrator._generate_response(result)
            self.chat_widget.add_message("Sourcer", response, "assistant")
            self.orchestrator.tts_service.speak(response)
            self.status_bar.showMessage("Analysis complete")
        else:
            self.status_bar.showMessage("Analysis failed")

    @pyqtSlot()
    def _on_clear_history(self) -> None:
        """Handle clear history action."""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear the conversation history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.orchestrator.clear_history()
            self.chat_widget.clear()
            self.status_bar.showMessage("History cleared")

    @pyqtSlot()
    def _on_repeat_last(self) -> None:
        """Handle repeat last response action."""
        self.orchestrator.repeat_last_response()
        self.status_bar.showMessage("Repeating last response")

    @pyqtSlot(bool)
    def _toggle_fullscreen(self, checked: bool) -> None:
        """Toggle fullscreen mode."""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    def _check_voice_input(self) -> None:
        """Check for voice input periodically."""
        if self.orchestrator.is_listening:
            text = self.orchestrator.process_voice_input()
            if text:
                self.chat_widget.add_message("You (voice)", text, "user")
                self._process_and_display_response()

    def _process_and_display_response(self) -> None:
        """Process current frame and display response."""
        result = self.orchestrator.analyze_current_frame()
        
        if result:
            # Update conversation history
            for entry in self.orchestrator.conversation_history:
                if entry not in self._displayed_history:
                    if entry["role"] == "assistant":
                        self.chat_widget.add_message("Sourcer", entry["content"], "assistant")
                    self._displayed_history.append(entry)

    def _update_ui(self) -> None:
        """Update UI elements periodically."""
        # Update webcam status
        if self.orchestrator.video_service.is_running:
            webcam_status = "Webcam: Active"
        else:
            webcam_status = "Webcam: Inactive"
        
        # Update model status
        if self.orchestrator.vision_service.is_initialized:
            model_status = "Models: Ready"
        else:
            model_status = "Models: Loading..."
        
        # Update status bar
        if not self.orchestrator.is_listening:
            self.status_bar.showMessage(f"{webcam_status} | {model_status}")

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Sourcer",
            f"<h2>Sourcer MVP</h2>"
            f"<p>Version {self.config.get('Application', 'version')}</p>"
            f"<p>A local AI visual assistant that helps you understand "
            f"your immediate environment through voice and text queries.</p>"
            f"<p>All processing happens locally on your device for privacy.</p>"
        )

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop timers
        self.voice_timer.stop()
        self.ui_timer.stop()
        
        # Clean up orchestrator
        self.orchestrator.cleanup()
        
        event.accept()