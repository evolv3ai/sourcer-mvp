```markdown
# Core Workflow / Sequence Diagrams

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Core Workflow / Sequence Diagrams".

### Voice Query Workflow [cite: 99]

```mermaid
sequenceDiagram
    participant User
    participant UI_Module as UI (PyQt)
    participant CoreOrchestrator as Orchestrator
    participant STT_Service as STT (Pipecat)
    participant Video_Service as VideoSvc
    participant Vision_Service as VisionSvc
    participant TTS_Service as TTS (Pipecat)

    User->>UI_Module: Activates voice input (e.g., clicks "Hold to Talk")
    UI_Module->>Orchestrator: notify_voice_input_start()
    Orchestrator->>STT_Service: start_transcription()
    Note over STT_Service: Pipecat manages mic audio stream

    loop Audio Streaming & Transcription
        User-->>STT_Service: Speaks query (audio stream) [cite: 100]
        STT_Service-->>Orchestrator: partial_transcription_update(text) [cite: 100]
        Orchestrator-->>UI_Module: display_partial_transcription(text) [cite: 100]
    end
    STT_Service->>Orchestrator: final_transcription(query_text) [cite: 100]
    Orchestrator->>UI_Module: display_final_query(query_text) [cite: 100]

    Orchestrator->>Video_Service: get_current_frame() [cite: 100]
    Video_Service->>Orchestrator: return frame_data [cite: 100]

    Orchestrator->>Vision_Service: analyze_frame(frame_data, query_text) [cite: 100]
    Note over Vision_Service: Runs YOLO, SAM (opt.), LLaVA [cite: 100]
    Vision_Service->>Orchestrator: return scene_description_text [cite: 100]

    Orchestrator->>UI_Module: display_response(scene_description_text) [cite: 100]
    Orchestrator->>TTS_Service: speak(scene_description_text) [cite: 100]
    Note over TTS_Service: Pipecat manages audio output

    TTS_Service-->>User: Spoken response [cite: 101]
```

### Text Query Workflow
```mermaid
sequenceDiagram
    participant User
    participant UI_Module as UI (PyQt)
    participant CoreOrchestrator as Orchestrator
    participant Video_Service as VideoSvc
    participant Vision_Service as VisionSvc
    participant TTS_Service as TTS (Pipecat)

    User->>UI_Module: Types query and hits Enter/Send
    UI_Module->>Orchestrator: process_text_query(query_text)
    Orchestrator->>UI_Module: display_final_query(query_text)

    Orchestrator->>Video_Service: get_current_frame()
    Video_Service->>Orchestrator: return frame_data

    Orchestrator->>Vision_Service: analyze_frame(frame_data, query_text)
    Note over Vision_Service: Runs YOLO, SAM (opt.), LLaVA
    Vision_Service->>Orchestrator: return scene_description_text [cite: 102]

    Orchestrator->>UI_Module: display_response(scene_description_text) [cite: 102]
    Orchestrator->>TTS_Service: speak(scene_description_text) [cite: 102]
    Note over TTS_Service: Pipecat manages audio output [cite: 102]

    TTS_Service-->>User: Spoken response [cite: 102]
```