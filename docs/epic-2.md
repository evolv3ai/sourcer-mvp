# Epic 2: Local Speech-to-Text (STT) Integration

> This document is a granulated shard from the main "Sourcer Product Requirements Document (PRD)" focusing on "Epic 2: Local Speech-to-Text (STT) Integration".

- **Goal:** Enable users to input queries using their voice, with the spoken words transcribed locally into text.
- **Story 3: As an AI Enthusiast, I want to use my voice to ask a question so that I can interact with Sourcer hands-free.**
    - Acceptance Criteria:
        - Application can capture audio from the default system microphone.
        - User-initiated voice input (e.g., via a "start listening" button or a defined activation phrase if feasible with Pipecat locally) is processed. [cite: 510]
        - The spoken words are transcribed into text by a local STT engine integrated via Pipecat. [cite: 511]
        - The transcribed text is displayed in the chat/log area.
        - STT processing latency is minimized. [cite: 512]
        - Notes for Architect/Scrum Master: Research and select a suitable local STT model for Pipecat. [cite: 513] UI needs clear indication of listening state. [cite: 514]