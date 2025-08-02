#!/usr/bin/env python3
"""Basic test to see if PyQt6 works."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    
    print("✓ PyQt6 imports successful")
    
    # Test basic app creation
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Sourcer MVP - Basic Test")
    window.resize(400, 300)
    
    label = QLabel("Sourcer MVP - Basic GUI Test\n\nIf you see this, PyQt6 is working!")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)
    
    print("✓ Basic PyQt6 application created successfully")
    print("✓ You should see a test window. Close it to continue.")
    
    window.show()
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)