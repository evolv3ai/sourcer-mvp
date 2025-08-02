"""Chat display widget."""

import logging
from datetime import datetime
from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont

from sourcer.utils.config_loader import ConfigLoader


class ChatWidget(QWidget):
    """Widget for displaying chat history."""
    
    # Signals
    message_added = pyqtSignal(str, str, str)  # sender, message, role
    
    def __init__(self, config: ConfigLoader, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the chat widget.
        
        Args:
            config: Configuration loader instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize UI
        self._init_ui()
        
        # Message count
        self.message_count = 0

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        
        layout.addWidget(self.chat_display)
        
        # Set up text formats
        self._setup_formats()

    def _setup_formats(self) -> None:
        """Set up text formatting styles."""
        # User message format
        self.user_format = QTextCharFormat()
        self.user_format.setForeground(QColor("#0066cc"))
        self.user_format.setFontWeight(QFont.Weight.Bold)
        
        # Assistant message format
        self.assistant_format = QTextCharFormat()
        self.assistant_format.setForeground(QColor("#009900"))
        self.assistant_format.setFontWeight(QFont.Weight.Bold)
        
        # Timestamp format
        self.timestamp_format = QTextCharFormat()
        self.timestamp_format.setForeground(QColor("#999999"))
        self.timestamp_format.setFontItalic(True)
        
        # Message body format
        self.body_format = QTextCharFormat()
        self.body_format.setForeground(QColor("#333333"))

    def add_message(self, sender: str, message: str, role: str = "user") -> None:
        """
        Add a message to the chat display.
        
        Args:
            sender: Message sender name
            message: Message content
            role: Role (user/assistant)
        """
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Add spacing between messages
        if self.message_count > 0:
            cursor.insertText("\n\n")
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cursor.insertText(f"[{timestamp}] ", self.timestamp_format)
        
        # Sender name with appropriate format
        if role == "user":
            cursor.insertText(f"{sender}: ", self.user_format)
        else:
            cursor.insertText(f"{sender}: ", self.assistant_format)
        
        # Message body
        cursor.insertText(message, self.body_format)
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
        
        self.message_count += 1
        
        # Emit signal
        self.message_added.emit(sender, message, role)
        
        self.logger.debug(f"Message added: {sender} ({role}): {message[:50]}...")

    def add_system_message(self, message: str) -> None:
        """
        Add a system message to the chat.
        
        Args:
            message: System message content
        """
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Add spacing
        if self.message_count > 0:
            cursor.insertText("\n\n")
        
        # System message format
        system_format = QTextCharFormat()
        system_format.setForeground(QColor("#666666"))
        system_format.setFontItalic(True)
        
        cursor.insertText(f"🔔 {message}", system_format)
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
        
        self.message_count += 1

    def clear(self) -> None:
        """Clear all messages from the chat."""
        self.chat_display.clear()
        self.message_count = 0
        self.logger.info("Chat history cleared")

    def get_history(self) -> str:
        """
        Get the chat history as plain text.
        
        Returns:
            Chat history as string
        """
        return self.chat_display.toPlainText()

    def save_history(self, filepath: str) -> bool:
        """
        Save chat history to a file.
        
        Args:
            filepath: Path to save the history
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.get_history())
            self.logger.info(f"Chat history saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save chat history: {e}")
            return False