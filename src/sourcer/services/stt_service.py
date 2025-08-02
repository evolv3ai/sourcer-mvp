"""Speech-to-Text service using Vosk via Pipecat."""

import json
import logging
import queue
import threading
from typing import Optional, Callable
from pathlib import Path

import sounddevice as sd
import vosk

from sourcer.utils.config_loader import ConfigLoader


class STTService:
    """Service for Speech-to-Text functionality."""

    def __init__(self, config: ConfigLoader) -> None:
        """
        Initialize the STT service.
        
        Args:
            config: Configuration loader instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Audio configuration
        self.sample_rate = self.config.get_int("Audio", "sample_rate", 16000)
        self.channels = self.config.get_int("Audio", "channels", 1)
        self.chunk_size = self.config.get_int("Audio", "chunk_size", 1024)
        self.silence_threshold = self.config.get_float("Audio", "silence_threshold", 0.01)
        self.timeout = self.config.get_float("Audio", "voice_activation_timeout", 3.0)
        
        # Vosk model
        self.model: Optional[vosk.Model] = None
        self.recognizer: Optional[vosk.KaldiRecognizer] = None
        
        # Audio stream
        self.audio_queue: queue.Queue = queue.Queue()
        self.is_listening = False
        self.stream: Optional[sd.InputStream] = None
        
        # Callbacks
        self.transcription_callback: Optional[Callable[[str], None]] = None

    def initialize(self) -> bool:
        """
        Initialize the STT service.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check for mock mode
            if self.config.get_bool("Development", "MOCK_MODELS", False):
                self.logger.info("Using mock STT mode")
                return True
            
            # Load Vosk model
            model_path = self.config.get_path("Models", "stt_model")
            if not model_path or not model_path.exists():
                self.logger.error(f"STT model not found at {model_path}")
                return False
            
            self.logger.info(f"Loading STT model from {model_path}")
            self.model = vosk.Model(str(model_path))
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            
            # Test audio device
            device_info = sd.query_devices(None, 'input')
            self.logger.info(f"Using audio device: {device_info['name']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize STT service: {e}")
            return False

    def start_listening(self, callback: Optional[Callable[[str], None]] = None) -> None:
        """
        Start listening for voice input.
        
        Args:
            callback: Optional callback for transcribed text
        """
        if self.is_listening:
            self.logger.warning("Already listening")
            return
        
        self.transcription_callback = callback
        self.is_listening = True
        
        # Start audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.chunk_size,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_audio)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        self.logger.info("Started listening for voice input")

    def stop_listening(self) -> None:
        """Stop listening for voice input."""
        self.is_listening = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        self.logger.info("Stopped listening")

    def _audio_callback(self, indata, frames, time, status) -> None:
        """
        Callback for audio stream.
        
        Args:
            indata: Input audio data
            frames: Number of frames
            time: Time info
            status: Stream status
        """
        if status:
            self.logger.warning(f"Audio stream status: {status}")
        
        # Add to queue for processing
        self.audio_queue.put(bytes(indata))

    def _process_audio(self) -> None:
        """Process audio data from queue."""
        while self.is_listening:
            try:
                # Get audio data with timeout
                audio_data = self.audio_queue.get(timeout=0.1)
                
                if self.recognizer:
                    # Process with Vosk
                    if self.recognizer.AcceptWaveform(audio_data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                        
                        if text:
                            self.logger.info(f"Transcribed: {text}")
                            if self.transcription_callback:
                                self.transcription_callback(text)
                    else:
                        # Partial result
                        partial = json.loads(self.recognizer.PartialResult())
                        partial_text = partial.get('partial', '')
                        if partial_text:
                            self.logger.debug(f"Partial: {partial_text}")
                
                elif self.config.get_bool("Development", "MOCK_MODELS", False):
                    # Mock mode - simulate transcription
                    self._mock_transcription()
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error processing audio: {e}")

    def _mock_transcription(self) -> None:
        """Simulate transcription in mock mode."""
        # Simulate occasional transcriptions
        import random
        if random.random() < 0.01:  # 1% chance per iteration
            mock_phrases = [
                "What do you see in front of me?",
                "Describe the scene",
                "What objects are visible?",
                "Tell me about my surroundings"
            ]
            text = random.choice(mock_phrases)
            self.logger.info(f"Mock transcribed: {text}")
            if self.transcription_callback:
                self.transcription_callback(text)

    def listen(self) -> Optional[str]:
        """
        Listen for a single utterance (blocking).
        
        Returns:
            Transcribed text or None
        """
        if not self.is_listening:
            return None
        
        # This is a simplified version - in production, you'd want
        # more sophisticated voice activity detection
        result_queue = queue.Queue()
        
        def callback(text: str) -> None:
            result_queue.put(text)
        
        # Temporarily set callback
        old_callback = self.transcription_callback
        self.transcription_callback = callback
        
        try:
            # Wait for result with timeout
            text = result_queue.get(timeout=self.timeout)
            return text
        except queue.Empty:
            return None
        finally:
            self.transcription_callback = old_callback

    def cleanup(self) -> None:
        """Clean up STT resources."""
        self.stop_listening()
        
        if self.recognizer:
            self.recognizer = None
        
        if self.model:
            self.model = None
        
        self.logger.info("STT service cleaned up")

    def get_status(self) -> dict:
        """
        Get STT service status.
        
        Returns:
            Status dictionary
        """
        return {
            "is_initialized": self.model is not None or self.config.get_bool("Development", "MOCK_MODELS", False),
            "is_listening": self.is_listening,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "model_loaded": self.model is not None
        }