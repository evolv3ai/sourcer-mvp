"""Core orchestrator that coordinates all services."""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from sourcer.services.video_service import VideoService
from sourcer.services.vision_service import VisionService
from sourcer.services.stt_service import STTService
from sourcer.services.tts_service import TTSService
from sourcer.utils.config_loader import ConfigLoader


@dataclass
class AnalysisResult:
    """Result of visual analysis."""
    timestamp: datetime
    image_data: Any  # numpy array
    objects_detected: list[Dict[str, Any]]
    scene_description: str
    confidence_scores: Dict[str, float]


class Orchestrator:
    """Main orchestrator that coordinates all AI services."""

    def __init__(self, config: ConfigLoader) -> None:
        """
        Initialize the orchestrator.
        
        Args:
            config: Configuration loader instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize services
        self.video_service = VideoService(config)
        self.vision_service = VisionService(config)
        self.stt_service = STTService(config)
        self.tts_service = TTSService(config)
        
        # State management
        self.is_listening = False
        self.last_analysis: Optional[AnalysisResult] = None
        self.conversation_history: list[Dict[str, Any]] = []
        
        self.logger.info("Orchestrator initialized")

    def start_services(self) -> None:
        """Start all services."""
        self.video_service.start()
        self.stt_service.initialize()
        self.tts_service.initialize()
        self.vision_service.initialize()
        
        self.logger.info("All services started")

    def stop_services(self) -> None:
        """Stop all services."""
        self.video_service.stop()
        self.stt_service.cleanup()
        self.tts_service.cleanup()
        self.vision_service.cleanup()
        
        self.logger.info("All services stopped")

    def process_voice_input(self) -> Optional[str]:
        """
        Process voice input from microphone.
        
        Returns:
            Transcribed text or None if no input
        """
        if not self.is_listening:
            return None
        
        text = self.stt_service.listen()
        if text:
            self.logger.info(f"Voice input transcribed: {text}")
            self._add_to_history("user", text, "voice")
        
        return text

    def process_text_input(self, text: str) -> None:
        """
        Process text input from user.
        
        Args:
            text: User input text
        """
        self.logger.info(f"Processing text input: {text}")
        self._add_to_history("user", text, "text")
        
        # Analyze current frame
        analysis = self.analyze_current_frame()
        if analysis:
            self._respond_with_analysis(analysis)

    def analyze_current_frame(self) -> Optional[AnalysisResult]:
        """
        Analyze the current webcam frame.
        
        Returns:
            Analysis result or None if failed
        """
        # Capture current frame
        frame = self.video_service.get_current_frame()
        if frame is None:
            self.logger.warning("No frame available from video service")
            return None
        
        # Run vision analysis
        try:
            # Detect objects
            detections = self.vision_service.detect_objects(frame)
            
            # Generate scene description
            description = self.vision_service.describe_scene(frame, detections)
            
            # Create analysis result
            result = AnalysisResult(
                timestamp=datetime.now(),
                image_data=frame,
                objects_detected=detections,
                scene_description=description,
                confidence_scores=self._calculate_confidence_scores(detections)
            )
            
            self.last_analysis = result
            self.logger.info(f"Frame analyzed: {len(detections)} objects detected")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error during frame analysis: {e}")
            return None

    def _respond_with_analysis(self, analysis: AnalysisResult) -> None:
        """Generate and speak response based on analysis."""
        response = self._generate_response(analysis)
        
        # Add to history
        self._add_to_history("assistant", response, "analysis")
        
        # Speak the response
        self.tts_service.speak(response)

    def _generate_response(self, analysis: AnalysisResult) -> str:
        """Generate natural language response from analysis."""
        if not analysis.objects_detected:
            return "I don't see any recognizable objects in the current view."
        
        # Build response
        response_parts = []
        
        # Main description
        response_parts.append(analysis.scene_description)
        
        # Object details
        object_counts: Dict[str, int] = {}
        for obj in analysis.objects_detected:
            label = obj.get("label", "unknown")
            object_counts[label] = object_counts.get(label, 0) + 1
        
        if object_counts:
            objects_str = ", ".join(
                f"{count} {label}{'s' if count > 1 else ''}"
                for label, count in object_counts.items()
            )
            response_parts.append(f"I can see {objects_str}.")
        
        return " ".join(response_parts)

    def _calculate_confidence_scores(self, detections: list[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average confidence scores by object type."""
        scores: Dict[str, list[float]] = {}
        
        for detection in detections:
            label = detection.get("label", "unknown")
            confidence = detection.get("confidence", 0.0)
            
            if label not in scores:
                scores[label] = []
            scores[label].append(confidence)
        
        # Calculate averages
        avg_scores = {}
        for label, confidences in scores.items():
            avg_scores[label] = sum(confidences) / len(confidences) if confidences else 0.0
        
        return avg_scores

    def _add_to_history(self, role: str, content: str, input_type: str) -> None:
        """Add entry to conversation history."""
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "role": role,
            "content": content,
            "type": input_type
        })

    def repeat_last_response(self) -> None:
        """Repeat the last assistant response."""
        for entry in reversed(self.conversation_history):
            if entry["role"] == "assistant":
                self.tts_service.speak(entry["content"])
                break

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
        self.last_analysis = None
        self.logger.info("Conversation history cleared")

    def toggle_listening(self) -> bool:
        """
        Toggle voice listening state.
        
        Returns:
            New listening state
        """
        self.is_listening = not self.is_listening
        self.logger.info(f"Listening state: {self.is_listening}")
        return self.is_listening

    def cleanup(self) -> None:
        """Clean up orchestrator resources."""
        self.stop_services()
        self.clear_history()