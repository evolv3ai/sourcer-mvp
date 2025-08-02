"""Text-to-Speech service using Piper via Pipecat."""

import logging
import queue
import threading
from typing import Optional
from pathlib import Path
import tempfile
import subprocess

import sounddevice as sd
import soundfile as sf
import numpy as np

from sourcer.utils.config_loader import ConfigLoader


class TTSService:
    """Service for Text-to-Speech functionality."""

    def __init__(self, config: ConfigLoader) -> None:
        """
        Initialize the TTS service.
        
        Args:
            config: Configuration loader instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Audio configuration
        self.sample_rate = self.config.get_int("Audio", "sample_rate", 16000)
        
        # Model path
        self.model_path: Optional[Path] = None
        self.is_initialized = False
        
        # Audio playback queue
        self.playback_queue: queue.Queue = queue.Queue()
        self.is_playing = False
        self.playback_thread: Optional[threading.Thread] = None

    def initialize(self) -> bool:
        """
        Initialize the TTS service.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check for mock mode
            if self.config.get_bool("Development", "MOCK_MODELS", False):
                self.logger.info("Using mock TTS mode")
                self.is_initialized = True
                return True
            
            # Get model path
            self.model_path = self.config.get_path("Models", "tts_model")
            if not self.model_path or not self.model_path.exists():
                self.logger.error(f"TTS model not found at {self.model_path}")
                return False
            
            # Test Piper availability
            try:
                result = subprocess.run(
                    ["piper", "--version"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    self.logger.error("Piper TTS not found. Please install piper-tts.")
                    return False
            except FileNotFoundError:
                self.logger.error("Piper TTS not found. Please install piper-tts.")
                return False
            
            # Start playback thread
            self.is_playing = True
            self.playback_thread = threading.Thread(target=self._playback_loop)
            self.playback_thread.daemon = True
            self.playback_thread.start()
            
            self.is_initialized = True
            self.logger.info("TTS service initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS service: {e}")
            return False

    def speak(self, text: str, wait: bool = False) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
            
        Returns:
            True if successful, False otherwise
        """
        if not text.strip():
            return True
        
        if not self.is_initialized:
            self.logger.error("TTS service not initialized")
            return False
        
        try:
            if self.config.get_bool("Development", "MOCK_MODELS", False):
                # Mock mode - just log
                self.logger.info(f"Mock TTS: {text}")
                return True
            
            # Generate audio file
            audio_data = self._generate_audio(text)
            if audio_data is None:
                return False
            
            # Add to playback queue
            self.playback_queue.put(audio_data)
            
            if wait:
                # Wait for queue to be empty
                self.playback_queue.join()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to speak text: {e}")
            return False

    def _generate_audio(self, text: str) -> Optional[np.ndarray]:
        """
        Generate audio from text using Piper.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio data as numpy array or None
        """
        try:
            # Create temporary file for output
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            # Run Piper
            cmd = [
                "piper",
                "--model", str(self.model_path),
                "--output_file", tmp_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                self.logger.error(f"Piper failed: {stderr}")
                return None
            
            # Load generated audio
            audio_data, sample_rate = sf.read(tmp_path)
            
            # Resample if necessary
            if sample_rate != self.sample_rate:
                # Simple resampling (for production, use a proper resampling library)
                factor = self.sample_rate / sample_rate
                new_length = int(len(audio_data) * factor)
                audio_data = np.interp(
                    np.linspace(0, len(audio_data), new_length),
                    np.arange(len(audio_data)),
                    audio_data
                )
            
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Failed to generate audio: {e}")
            return None

    def _playback_loop(self) -> None:
        """Playback loop running in separate thread."""
        while self.is_playing:
            try:
                # Get audio data with timeout
                audio_data = self.playback_queue.get(timeout=0.1)
                
                # Play audio
                sd.play(audio_data, self.sample_rate)
                sd.wait()  # Wait for playback to complete
                
                self.playback_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Playback error: {e}")

    def stop(self) -> None:
        """Stop any ongoing speech."""
        # Clear queue
        while not self.playback_queue.empty():
            try:
                self.playback_queue.get_nowait()
                self.playback_queue.task_done()
            except queue.Empty:
                break
        
        # Stop current playback
        sd.stop()

    def cleanup(self) -> None:
        """Clean up TTS resources."""
        self.is_playing = False
        self.stop()
        
        if self.playback_thread:
            self.playback_thread.join(timeout=2.0)
        
        self.logger.info("TTS service cleaned up")

    def get_status(self) -> dict:
        """
        Get TTS service status.
        
        Returns:
            Status dictionary
        """
        return {
            "is_initialized": self.is_initialized,
            "model_loaded": self.model_path is not None,
            "queue_size": self.playback_queue.qsize(),
            "sample_rate": self.sample_rate
        }

    def set_voice_parameters(self, speed: float = 1.0, pitch: float = 1.0) -> None:
        """
        Set voice parameters (for future enhancement).
        
        Args:
            speed: Speech speed multiplier
            pitch: Pitch adjustment
        """
        # This would require more advanced audio processing
        # For now, just log the request
        self.logger.info(f"Voice parameters requested: speed={speed}, pitch={pitch}")
        # TODO: Implement voice parameter adjustment