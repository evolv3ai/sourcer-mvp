# Epic 5: Basic UI Controls and Fallback Input

> This document is a granulated shard from the main "Sourcer Product Requirements Document (PRD)" focusing on "Epic 5: Basic UI Controls and Fallback Input".

- **Goal:** Provide essential UI controls for basic interaction and a fallback text input method.
- **Story 8: As an AI Enthusiast, I want a button or mechanism to explicitly trigger voice input listening so that I have control over when the microphone is active.**
    - Acceptance Criteria:
        - A clear UI element (e.g., "Hold to Talk" button, "Click to Ask" button) exists to initiate voice input.
        - The microphone is only active for STT when explicitly engaged by the user via this control.
        - Visual feedback indicates when the application is listening. [cite: 538]
- **Story 9: As an AI Enthusiast, I want to be able to type my query into a text field as an alternative to voice so that I can use the application if voice input is problematic or not preferred.**
    - Acceptance Criteria:
        - A text input field is available in the UI.
        - Users can type a query and submit it (e.g., by pressing Enter or clicking a 'Send' button).
        - Typed queries trigger the same local visual analysis and response flow as voice queries.
        - The typed query and subsequent response appear in the chat/log history.