# src/sourcer/ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QLineEdit, QFrame
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sourcer MVP")
        self.setGeometry(100, 100, 1024, 768)
        self.setMinimumSize(800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main vertical layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # 1. Webcam Display Area (Top)
        self.webcam_area = QFrame()
        self.webcam_area.setFrameShape(QFrame.Shape.StyledPanel)
        self.webcam_area.setStyleSheet("background-color: #333; border: 1px solid #555;")
        webcam_layout = QVBoxLayout(self.webcam_area) # Layout for the webcam area
        webcam_label = QLabel("Webcam Feed Area")
        webcam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        webcam_label.setStyleSheet("color: white;")
        webcam_layout.addWidget(webcam_label)
        self.main_layout.addWidget(self.webcam_area, stretch=3) # Takes more space

        # 2. Bottom Section (Horizontal Layout for Chat and Input)
        self.bottom_section_layout = QHBoxLayout()

        # 2a. Chat/Log History Area (Bottom Left)
        self.chat_log_area = QTextEdit()
        self.chat_log_area.setReadOnly(True)
        self.chat_log_area.setPlaceholderText("Chat and event logs will appear here...")
        self.chat_log_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.bottom_section_layout.addWidget(self.chat_log_area, stretch=2) # Give it more space than input

        # 2b. Input Control Area (Bottom Right)
        self.input_control_area = QFrame()
        self.input_control_area.setFrameShape(QFrame.Shape.StyledPanel)
        self.input_control_area.setStyleSheet("background-color: #e0e0e0; border: 1px solid #bbb;")
        input_area_layout = QVBoxLayout(self.input_control_area) # Layout for input controls
        
        input_area_label = QLabel("Input Controls")
        input_area_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_area_layout.addWidget(input_area_label)

        self.text_input_field = QLineEdit()
        self.text_input_field.setPlaceholderText("Type your message here...")
        input_area_layout.addWidget(self.text_input_field)
        # Add other input controls here in future stories (e.g., voice button)
        input_area_layout.addStretch(1) # Pushes controls to the top if area is larger

        self.bottom_section_layout.addWidget(self.input_control_area, stretch=1)

        # Add bottom section to the main layout
        self.main_layout.addLayout(self.bottom_section_layout, stretch=1) # Takes less space

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
