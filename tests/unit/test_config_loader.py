"""Unit tests for ConfigLoader."""

import os
import tempfile
from pathlib import Path
import pytest

from sourcer.utils.config_loader import ConfigLoader


class TestConfigLoader:
    """Test cases for ConfigLoader."""

    @pytest.fixture
    def temp_config_file(self):
        """Create a temporary config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""[Application]
name = Test App
version = 1.0.0
debug = false

[UI]
window_width = 800
window_height = 600
webcam_fps = 30.5

[Vision]
target_objects = person,chair,table
confidence_threshold = 0.75
""")
            temp_path = Path(f.name)
        
        yield temp_path
        
        # Cleanup
        temp_path.unlink(missing_ok=True)

    def test_load_config(self, temp_config_file):
        """Test loading configuration from file."""
        config = ConfigLoader(temp_config_file)
        
        assert config.get("Application", "name") == "Test App"
        assert config.get("Application", "version") == "1.0.0"

    def test_get_with_fallback(self, temp_config_file):
        """Test getting values with fallback."""
        config = ConfigLoader(temp_config_file)
        
        # Existing value
        assert config.get("Application", "name", "Default") == "Test App"
        
        # Non-existing value
        assert config.get("Application", "missing", "Default") == "Default"
        
        # Non-existing section
        assert config.get("Missing", "key", "Default") == "Default"

    def test_get_int(self, temp_config_file):
        """Test getting integer values."""
        config = ConfigLoader(temp_config_file)
        
        assert config.get_int("UI", "window_width") == 800
        assert config.get_int("UI", "window_height") == 600
        assert config.get_int("UI", "missing", 100) == 100

    def test_get_float(self, temp_config_file):
        """Test getting float values."""
        config = ConfigLoader(temp_config_file)
        
        assert config.get_float("UI", "webcam_fps") == 30.5
        assert config.get_float("Vision", "confidence_threshold") == 0.75
        assert config.get_float("UI", "missing", 1.5) == 1.5

    def test_get_bool(self, temp_config_file):
        """Test getting boolean values."""
        config = ConfigLoader(temp_config_file)
        
        assert config.get_bool("Application", "debug") is False
        assert config.get_bool("Application", "missing", True) is True

    def test_get_list(self, temp_config_file):
        """Test getting list values."""
        config = ConfigLoader(temp_config_file)
        
        objects = config.get_list("Vision", "target_objects")
        assert objects == ["person", "chair", "table"]
        
        assert config.get_list("Vision", "missing", ["default"]) == ["default"]

    def test_environment_override(self, temp_config_file, monkeypatch):
        """Test environment variable override."""
        config = ConfigLoader(temp_config_file)
        
        # Set environment variable
        monkeypatch.setenv("APPLICATION_NAME", "Overridden App")
        
        # Environment variable should override config file
        assert config.get("Application", "name") == "Overridden App"

    def test_parse_value(self, temp_config_file):
        """Test value parsing."""
        config = ConfigLoader(temp_config_file)
        
        # Boolean parsing
        assert config._parse_value("true") is True
        assert config._parse_value("false") is False
        assert config._parse_value("True") is True
        
        # Integer parsing
        assert config._parse_value("123") == 123
        assert config._parse_value("-456") == -456
        
        # Float parsing
        assert config._parse_value("12.34") == 12.34
        assert config._parse_value("-56.78") == -56.78
        
        # String parsing
        assert config._parse_value("hello world") == "hello world"