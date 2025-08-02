### Text Query Workflow

- **Goal:** The user wants to ask a question about the objects visible in the webcam feed by typing their query and receive a spoken and text-based answer.

- **Assumptions:**
    - The application is running, and the main window is visible.
    - The webcam is active and displaying a live feed in the `WebcamDisplayWidget`.

- **Steps / Diagram:**

  ```mermaid
  graph TD
      A[Start: User views webcam feed] --> B{User decides to ask a text query};
      B --> C["User types query into 'Text Input Field'"];
      C --> D["User clicks 'Send/Activate Button' or presses Enter key"];
      D --> E["UI: User's query appears in Chat/Log Area (e.g., as 'You: What is that blue object near the window?')"];
      E --> F["UI: Text Input Field is cleared. Focus may return to Text Input Field for subsequent queries."];
      F --> G["UI: 'Send/Activate Button' may briefly show a 'Processing' state or become temporarily disabled (subtle feedback)"];
      G --> H["Core Orchestrator receives query text"];
      H --> I["Core Orchestrator captures current frame from Video Input Handler"];
      I --> J["Core Orchestrator sends frame and query text to Local Vision Pipeline"];
      J -- Analysis --> K["Local Vision Pipeline (YOLO, SAM, LLaVA) processes image and text"];
      K -- Textual Description --> L["Core Orchestrator receives textual description"];
      L --> M["UI: System's response appears in Chat/Log Area (e.g., 'Sourcer: The blue object near the window is a book.')"];
      L -- Textual Description --> N["System: Local TTS Service (Pipecat) converts text to speech"];
      N -- Spoken Response --> O["User hears spoken response"];
      O --> P["UI: 'Send/Activate Button' returns to normal state (if changed)"];
      P --> Q[End: User has received visual and auditory response];

      %% Error Flows & Edge Cases from Vision Pipeline (same as voice query)
      K -- Vision Analysis Error --> K_Err1["UI: Show message in Chat/Log Area (e.g., 'Error analyzing the scene. Please try again.')"];
      K_Err1 --> P;
      K -- No Objects Detected/Relevant Info --> K_Err2["UI: Show message in Chat/Log Area (e.g., 'I don't see any relevant objects.' or 'I couldn't identify that.')"];
      K_Err2 -- Textual Description (e.g., "I don't see...") --> N; %% TTS still speaks the "don't see" message

      %% Error Flows & Edge Cases from TTS (same as voice query)
      N -- TTS Failure --> N_Err1["UI: Response still appears in Chat/Log. Optionally show subtle TTS error icon/message."];
      N_Err1 --> O_Silent[User reads response, no spoken audio];
      O_Silent --> P;
  ```

  - **Detailed Steps and UI Feedback:**

    1.  **User Initiates Text Query:**
          * **Action:** User types their query into the `Text Input Field`.
          * **UI Feedback:** Standard text input behavior.
    2.  **User Submits Query:**
          * **Action:** User clicks the "Send/Activate Button" or presses the Enter key in the `Text Input Field`.
          * **UI Feedback:**
              * The query text immediately appears in the `ChatLogWidget`, attributed to the user (e.g., "You: [typed query]").
              * The `Text Input Field` is cleared to ready it for a new query.
              * Optionally, the "Send/Activate Button" could dim or show a very brief "Sending..." state, then return to active. This provides feedback that the submission was registered.
              * Focus should ideally return to the `Text Input Field`.
    3.  **Vision Pipeline Processing:**
          * **System Action:** Core Orchestrator sends the query and current webcam frame to the vision pipeline.
          * **UI Feedback:** While processing, a subtle visual cue might be helpful if analysis takes more than a split second. This could be a temporary change in the "Send/Activate Button" (e.g., a gentle pulsing or a temporary "Processing..." label if the button is wide enough) or a small, unobtrusive global status indicator if one exists. For MVP, keeping it minimal is acceptable if the response is quick. [Source: 12]
    4.  **Response Generation & Display:**
          * **System Action:** Vision pipeline returns a textual description. Core Orchestrator sends it to UI and TTS.
          * **UI Feedback:**
              * The system's textual response appears in the `ChatLogWidget` (e.g., "Sourcer: [response text]").
              * Any "Processing" indicator on the "Send/Activate Button" or elsewhere returns to normal.
          * **Auditory Feedback:** User hears the spoken response via TTS.

  - **Error Handling & Edge Cases (Text Query):**

      * **Empty Query Submission:**
          * **Trigger:** User clicks "Send/Activate Button" or presses Enter with no text in the `Text Input Field`.
          * **UI Feedback:**
              * The system should ideally do nothing, or provide a very subtle, non-blocking cue (e.g., a slight shake of the input field or brief border highlight) to indicate input is expected. No error message in chat log needed.
              * The `Text Input Field` remains in focus.
      * **Vision Analysis Error:** (Same as Voice Query Workflow)
          * **Trigger:** The local vision pipeline encounters an unrecoverable error.
          * **UI Feedback:** Message in `ChatLogWidget` (e.g., "Sourcer: I encountered a problem analyzing the scene. Please try again."). This is spoken via TTS.
      * **No Objects Detected / Nothing Relevant to Query:** (Same as Voice Query Workflow)
          * **Trigger:** Vision pipeline finds no relevant information.
          * **UI Feedback:** Message in `ChatLogWidget` (e.g., "Sourcer: I don't see any [queried objects] in the view."). This is spoken via TTS.
      * **TTS Failure:** (Same as Voice Query Workflow)
          * **Trigger:** TTS service fails.
          * **UI Feedback:** Textual response still displayed in `ChatLogWidget`. Optional subtle cue for TTS failure.