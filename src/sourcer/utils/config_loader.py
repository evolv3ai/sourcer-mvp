"""Configuration loader utility."""

import os
import configparser
from pathlib import Path
from typing import Any, Optional, Union

from dotenv import load_dotenv


class ConfigLoader:
    """Load and manage application configuration."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration file. If None, uses default.
        """
        # Load environment variables
        load_dotenv()
        
        # Set up config path
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            config_path = project_root / "config" / "settings.ini"
        
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            self.config.read(self.config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            fallback: Default value if not found
            
        Returns:
            Configuration value or fallback
        """
        # First check environment variables
        env_key = f"{section.upper()}_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._parse_value(env_value)
        
        # Then check config file
        try:
            value = self.config.get(section, key)
            return self._parse_value(value)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get an integer configuration value."""
        value = self.get(section, key, fallback)
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get a float configuration value."""
        value = self.get(section, key, fallback)
        try:
            return float(value)
        except (TypeError, ValueError):
            return fallback

    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get a boolean configuration value."""
        value = self.get(section, key, fallback)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return fallback

    def get_list(self, section: str, key: str, fallback: Optional[list] = None) -> list:
        """Get a list configuration value (comma-separated)."""
        value = self.get(section, key)
        if value is None:
            return fallback or []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return fallback or []

    def get_path(self, section: str, key: str, fallback: Optional[Path] = None) -> Optional[Path]:
        """Get a path configuration value."""
        value = self.get(section, key)
        if value is None:
            return fallback
        path = Path(value)
        
        # If relative path, make it relative to project root
        if not path.is_absolute():
            project_root = Path(__file__).parent.parent.parent.parent
            path = project_root / path
        
        return path

    def _parse_value(self, value: str) -> Union[str, int, float, bool]:
        """Parse a string value into appropriate type."""
        # Try to parse as boolean
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        
        # Try to parse as int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try to parse as float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value

    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()