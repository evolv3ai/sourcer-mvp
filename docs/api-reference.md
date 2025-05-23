# API Reference

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "API Reference".

### External APIs Consumed (N/A for Core MVP Functionality)

For the core MVP functionality, all processing is local, and no external APIs are consumed. [cite: 83] Future enhancements might introduce them. [cite: 84]

### Internal APIs Provided (Conceptual Internal Interfaces)

While not external APIs in the web sense, the modules within the application will interact through well-defined Python class/method interfaces: [cite: 84]

  - **`CoreOrchestrator` Interface:**
      - `process_query(query_text: str, frame: FrameData) -> str`: Takes text query and frame, returns textual description.
      - `handle_voice_input(audio_chunk: bytes)`: Processes audio for STT. [cite: 85]
      - `get_spoken_response(text: str) -> AudioData`: Converts text to speakable audio.
  - **`VideoService` Interface:**
      - `start_capture() -> bool` [cite: 86]
      - `stop_capture()` [cite: 86]
      - `get_current_frame() -> Optional[FrameData]` [cite: 86]
      - `register_frame_callback(callback_fn)` [cite: 86]
  - **`VisionService` Interface:**
      - `analyze_frame(frame: FrameData, query_context: Optional[str] = None) -> str`: Analyzes frame using YOLO, SAM (optional), LLaVA.
  - **`STTService (via Pipecat)` Interface:**
      - Conceptual: Pipecat provides services to stream audio and receive transcriptions. The `CoreOrchestrator` will use Pipecat's Python client library. [cite: 88]
  - **`TTSService (via Pipecat)` Interface:**
      - Conceptual: Pipecat provides services to send text and receive/play audio. The `CoreOrchestrator` will use Pipecat's Python client library. [cite: 89]