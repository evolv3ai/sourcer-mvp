"""User interface components."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow

__all__ = ["MainWindow"]