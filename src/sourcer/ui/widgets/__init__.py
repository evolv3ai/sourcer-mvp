"""Custom UI widgets."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .webcam_widget import WebcamWidget
    from .chat_widget import ChatWidget

__all__ = [
    "WebcamWidget",
    "ChatWidget",
]