# src/sourcer/app.py
import sys
from PyQt6.QtWidgets import QApplication
# We'll create main_window.py in the next step, so the import will eventually work.
from .ui.main_window import MainWindow 

class SourcerApp:
    def __init__(self):
        print("SourcerApp initialized") # Updated print statement
        # self.main_window will be fully initialized in run()
        # For now, we just ensure the class is aware of MainWindow
        self.main_window_class = MainWindow 

    def run(self):
        print("SourcerApp run") # Updated print statement
        qt_app = QApplication(sys.argv)
        
        # Instantiate the main window using the class stored in __init__
        self.window = self.main_window_class() 
        self.window.show()
        
        sys.exit(qt_app.exec())
