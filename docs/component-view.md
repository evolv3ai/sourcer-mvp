# Component View

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Component View and Architectural Patterns".

The application consists of several major logical components within the monolithic structure:

  - **User Interface (UI) Module (PyQt-based):** [cite: 30]
      - **Responsibility:** Handles all user interactions, including displaying the webcam feed, chat/log history, text input fields, and microphone status indicators. It captures user input (voice commands, typed text) and presents output (textual and visual feedback).
      - Key Sub-components: [cite: 32]
          - `MainWindow`: Main application window.
          - `WebcamDisplayWidget`: Renders the live webcam feed. [cite: 33]
          - `ChatLogWidget`: Displays conversation history.
          - `InputControlWidget`: Manages text input and voice activation control. [cite: 34]

  - **Video Input Handler Module:** [cite: 34]
      - **Responsibility:** Accesses the default system webcam, captures video frames, and provides them to the UI for display and to the vision pipeline for analysis. Handles scenarios like webcam not found or access denied. [cite: 35]

  - **Core Orchestrator Module (Python / Pipecat):** [cite: 35]
      - **Responsibility:** The central nervous system of the application. It receives queries (transcribed voice or text), triggers the vision pipeline with the current webcam frame, receives the textual description, and coordinates sending it to the UI and the TTS service. Manages the overall flow of interaction. Pipecat will be instrumental in managing the STT and TTS pipeline segments. [cite: 37]
  - **Local Vision Pipeline Module (Python):** [cite: 38]
      - **Responsibility:** Performs the visual analysis. This module integrates and orchestrates the local AI models: [cite: 39]
          - `YOLOModelWrapper`: For object detection from the webcam frame.
          - `MobileSAMModelWrapper`: For potential segmentation tasks to provide context or focus for LLaVA (use determined by LLaVA's needs and performance trade-offs).
          - `LLaVAModelWrapper`: For generating textual descriptions of the scene/objects based on the frame and potentially inputs from YOLO/SAM.
      - Ensures all model execution is local. [cite: 42]

  - **Local STT Service (Integrated via Pipecat):** [cite: 42]
      - **Responsibility:** Transcribes spoken user queries into text using a local STT engine. Pipecat will manage the audio input stream and interaction with the chosen STT engine.
  - **Local TTS Service (Integrated via Pipecat):** [cite: 44]
      - **Responsibility:** Converts textual descriptions from the vision pipeline into spoken audio responses using a local TTS engine. Pipecat will manage sending text to the TTS engine and playing back the audio.
  - **Configuration & Resource Management Module:** [cite: 46]
      - **Responsibility:** Manages application settings (though minimal for MVP), paths to AI models, and other necessary resources. Handles loading and initialization of AI models. [cite: 47]

```mermaid
graph TD
    subgraph UI_Module ["User Interface (PyQt)"] [cite: 47]
        direction LR
        MW[MainWindow]
        WDW[WebcamDisplayWidget]
        CLW[ChatLogWidget]
        ICW[InputControlWidget]
        MW --> WDW
        MW --> CLW
        MW --> ICW
    end

    subgraph Core_Services ["Core Services (Python/Pipecat)"]
        direction LR
        CO[CoreOrchestrator]
        STT_Service[Local STT Service]
        TTS_Service[Local TTS Service]
        VP[Local Vision Pipeline]
        VIH[VideoInputHandler]
        CRM[Config & Resource Mgmt]
        CO --> STT_Service
        CO --> TTS_Service
        CO --> VP
        CO --> VIH
        CO --> CRM
    end

    subgraph Vision_Pipeline_Internal ["Vision Pipeline Detail"] [cite: 49]
        direction LR
        YOLO[YOLOModelWrapper]
        SAM[MobileSAMModelWrapper]
        LLaVA[LLaVAModelWrapper]
        VP --> YOLO
        VP --> SAM
        VP --> LLaVA
        YOLO --> LLaVA [cite: 50]
        SAM --> LLaVA
    end

    UI_Module -- User Input / Control --> CO;
    VIH -- Raw Video Frames --> UI_Module; [cite: 51]
    VIH -- Analysis Frame --> CO; [cite: 51]
    CO -- Text for UI --> UI_Module;
    STT_Service -- Transcribed Text --> CO; [cite: 52]
    VP -- Textual Description --> CO;
    TTS_Service -- Audio Output --> UserDeviceAudio[User Device Audio Output]; [cite: 53]

    UserDeviceAudio --> User; [cite: 53]
    UI_Module --> User;
	
```
	### Architectural / Design Patterns Adopted

	-   **Monolithic Application:** Chosen for MVP simplicity, reducing deployment and inter-service communication overhead.
	-   **Model-View-Controller (MVC) or Model-View-Presenter (MVP) variants (Conceptual for UI):** The PyQt UI will be structured to separate display logic (View), user input handling (Controller/Presenter), and application data/state (Model, managed by the Core Orchestrator and other services).
	**Service Orchestration (via Pipecat for Voice):** Pipecat will orchestrate the voice input (STT) and voice output (TTS) parts of the pipeline. The Core Orchestrator module will handle the broader application logic.
	-   **Wrapper/Adapter Pattern:** Each AI model (YOLO, SAM, LLaVA, STT, TTS) will be wrapped in a dedicated Python class/module. This isolates the core application from the specifics of each model's API, making it easier to swap models or update versions.
	-   **Event-Driven (Partially):** UI interactions (button clicks, voice activation) will trigger events that are handled by the application logic. Pipecat itself is event-driven for handling voice streams.
	-   **Singleton (for Model Management):** AI models, being resource-intensive, will likely be loaded once and accessed via a singleton-like pattern or a dedicated resource manager to avoid redundant loading.

<!-- end list -->