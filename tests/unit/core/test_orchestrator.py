"""Unit tests for Orchestrator."""

from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
import pytest

from sourcer.core.orchestrator import Orchestrator, AnalysisResult
from sourcer.utils.config_loader import ConfigLoader


class TestOrchestrator:
    """Test cases for Orchestrator."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        config = Mock(spec=ConfigLoader)
        config.get.return_value = "test_value"
        config.get_int.return_value = 10
        config.get_float.return_value = 0.5
        config.get_bool.return_value = True
        config.get_list.return_value = ["person", "chair"]
        return config

    @pytest.fixture
    def orchestrator(self, mock_config):
        """Create orchestrator with mocked services."""
        with patch('sourcer.core.orchestrator.VideoService'), \
             patch('sourcer.core.orchestrator.VisionService'), \
             patch('sourcer.core.orchestrator.STTService'), \
             patch('sourcer.core.orchestrator.TTSService'):
            return Orchestrator(mock_config)

    def test_initialization(self, orchestrator):
        """Test orchestrator initialization."""
        assert orchestrator.is_listening is False
        assert orchestrator.last_analysis is None
        assert orchestrator.conversation_history == []

    def test_start_services(self, orchestrator):
        """Test starting all services."""
        orchestrator.start_services()
        
        orchestrator.video_service.start.assert_called_once()
        orchestrator.stt_service.initialize.assert_called_once()
        orchestrator.tts_service.initialize.assert_called_once()
        orchestrator.vision_service.initialize.assert_called_once()

    def test_stop_services(self, orchestrator):
        """Test stopping all services."""
        orchestrator.stop_services()
        
        orchestrator.video_service.stop.assert_called_once()
        orchestrator.stt_service.cleanup.assert_called_once()
        orchestrator.tts_service.cleanup.assert_called_once()
        orchestrator.vision_service.cleanup.assert_called_once()

    def test_process_voice_input_not_listening(self, orchestrator):
        """Test voice input when not listening."""
        orchestrator.is_listening = False
        result = orchestrator.process_voice_input()
        
        assert result is None
        orchestrator.stt_service.listen.assert_not_called()

    def test_process_voice_input_listening(self, orchestrator):
        """Test voice input when listening."""
        orchestrator.is_listening = True
        orchestrator.stt_service.listen.return_value = "test voice input"
        
        result = orchestrator.process_voice_input()
        
        assert result == "test voice input"
        assert len(orchestrator.conversation_history) == 1
        assert orchestrator.conversation_history[0]["content"] == "test voice input"
        assert orchestrator.conversation_history[0]["role"] == "user"
        assert orchestrator.conversation_history[0]["type"] == "voice"

    def test_process_text_input(self, orchestrator):
        """Test processing text input."""
        # Mock the analysis methods
        mock_analysis = AnalysisResult(
            timestamp=datetime.now(),
            image_data=None,
            objects_detected=[{"label": "person", "confidence": 0.9}],
            scene_description="A person is visible",
            confidence_scores={"person": 0.9}
        )
        
        orchestrator.analyze_current_frame = Mock(return_value=mock_analysis)
        orchestrator._respond_with_analysis = Mock()
        
        orchestrator.process_text_input("test input")
        
        assert len(orchestrator.conversation_history) == 1
        assert orchestrator.conversation_history[0]["content"] == "test input"
        orchestrator.analyze_current_frame.assert_called_once()
        orchestrator._respond_with_analysis.assert_called_once_with(mock_analysis)

    def test_analyze_current_frame_no_frame(self, orchestrator):
        """Test frame analysis when no frame available."""
        orchestrator.video_service.get_current_frame.return_value = None
        
        result = orchestrator.analyze_current_frame()
        
        assert result is None

    def test_analyze_current_frame_success(self, orchestrator):
        """Test successful frame analysis."""
        import numpy as np
        
        # Mock frame
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        orchestrator.video_service.get_current_frame.return_value = mock_frame
        
        # Mock detections
        mock_detections = [
            {"label": "person", "confidence": 0.9, "bbox": {"x1": 10, "y1": 10, "x2": 100, "y2": 100}}
        ]
        orchestrator.vision_service.detect_objects.return_value = mock_detections
        orchestrator.vision_service.describe_scene.return_value = "A person is visible"
        
        result = orchestrator.analyze_current_frame()
        
        assert result is not None
        assert isinstance(result, AnalysisResult)
        assert result.objects_detected == mock_detections
        assert result.scene_description == "A person is visible"
        assert result.confidence_scores == {"person": 0.9}

    def test_generate_response_no_objects(self, orchestrator):
        """Test response generation with no objects."""
        analysis = AnalysisResult(
            timestamp=datetime.now(),
            image_data=None,
            objects_detected=[],
            scene_description="",
            confidence_scores={}
        )
        
        response = orchestrator._generate_response(analysis)
        
        assert response == "I don't see any recognizable objects in the current view."

    def test_generate_response_with_objects(self, orchestrator):
        """Test response generation with objects."""
        analysis = AnalysisResult(
            timestamp=datetime.now(),
            image_data=None,
            objects_detected=[
                {"label": "person", "confidence": 0.9},
                {"label": "chair", "confidence": 0.8},
                {"label": "chair", "confidence": 0.7}
            ],
            scene_description="A workspace scene",
            confidence_scores={"person": 0.9, "chair": 0.75}
        )
        
        response = orchestrator._generate_response(analysis)
        
        assert "A workspace scene" in response
        assert "1 person" in response
        assert "2 chairs" in response

    def test_toggle_listening(self, orchestrator):
        """Test toggling listening state."""
        assert orchestrator.is_listening is False
        
        state1 = orchestrator.toggle_listening()
        assert state1 is True
        assert orchestrator.is_listening is True
        
        state2 = orchestrator.toggle_listening()
        assert state2 is False
        assert orchestrator.is_listening is False

    def test_clear_history(self, orchestrator):
        """Test clearing conversation history."""
        # Add some history
        orchestrator.conversation_history = [
            {"role": "user", "content": "test1"},
            {"role": "assistant", "content": "test2"}
        ]
        orchestrator.last_analysis = Mock()
        
        orchestrator.clear_history()
        
        assert orchestrator.conversation_history == []
        assert orchestrator.last_analysis is None

    def test_repeat_last_response(self, orchestrator):
        """Test repeating last response."""
        orchestrator.conversation_history = [
            {"role": "user", "content": "question"},
            {"role": "assistant", "content": "answer"},
            {"role": "user", "content": "another question"}
        ]
        
        orchestrator.repeat_last_response()
        
        orchestrator.tts_service.speak.assert_called_once_with("answer")