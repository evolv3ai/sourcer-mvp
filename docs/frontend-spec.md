## Interaction & Usability Specifications

This section details the interaction behaviors for UI elements and visual feedback mechanisms for system states, ensuring a usable and intuitive experience within the PyQt6 application.

### General Interaction Principles

-   **Responsiveness:** Every user action on an interactive element (button click, text input) will provide immediate visual feedback (e.g., button pressed state, text appearing). System processing will be indicated clearly.
-   **Forgiveness:** Users can easily correct input errors (e.g., backspace in text fields, clearing text). Accidental destructive actions are not a primary concern for MVP's core query functionality.
-   **Consistency:** Interaction patterns are consistent across the application. For instance, buttons will have similar hover/pressed states.
-   **Feedback:** The system will clearly communicate its current state (idle, listening, processing, error) through the mechanisms detailed below.

### Specific UI Element Interactions

-   **`MainWindow` (Main Application Window):**
    * Standard window behaviors: open, close, minimize, maximize, resize.
    * On resize, internal components should adjust their layout and size appropriately (e.g., `WebcamDisplayWidget` and `ChatLogWidget` should scale, `InputControlWidget` might maintain fixed height but adjust width).
    * On close, the application should terminate gracefully.

-   **`WebcamDisplayWidget`:**
    * Primarily a passive display area for the live webcam feed.
    * No direct user interaction (e.g., click, drag) is expected on the feed itself for MVP.
    * If the webcam is unavailable or permissions are denied, a static message (e.g., "Webcam not available. Please check connection and permissions.") will be displayed centrally within this widget's area. The application should still be usable for text queries if the vision pipeline can operate on a placeholder or last valid frame (TBD by backend capabilities – for UI, assume it shows error and other functions may be limited).

-   **`ChatLogWidget`:**
    * **Scrolling:**
        * Automatically scrolls to the most recent message when a new query or response is added.
        * Users can manually scroll up to review older messages using a standard vertical scrollbar (which appears only when content overflows).
        * Mouse wheel scrolling should be supported when the mouse is over this widget.
    * **Text Selection:** Users should be able to select text within the chat log entries for copying (standard `QTextBrowser` or similar widget behavior).
    * **Content Display:** Queries and responses are clearly attributed (e.g., "You: [query]", "Sourcer: [response]") and visually distinct (e.g., alignment, subtle background differences as per mockups).

-   **`InputControlWidget`:**
    * **`MicrophoneActivationControl` (`QPushButton` with icon):**
        * **Interaction Model:** "Click to Start / Click to Stop" voice input.
            * **First Click (when Idle):** Initiates voice input. `MicrophoneStatusIndicator` changes to 'Listening'.
            * **Second Click (when Listening or Processing STT):** Stops voice input/cancels STT. `MicrophoneStatusIndicator` changes to 'Idle' (or 'Processing' briefly if STT had captured audio before stop, then 'Idle').
        * **Visual Feedback:** Button shows a standard pressed state on click. Icon color/style changes according to `MicrophoneStatusIndicator` states.
        * **Tooltip:** "Start/Stop Voice Query".
    * **`MicrophoneStatusIndicator` (Visual cue integrated or adjacent to `MicrophoneActivationControl`):**
        * **Idle:** Default state (e.g., gray microphone icon or gray dot).
        * **Listening:** Active state (e.g., blue microphone icon, "Listening..." label, or blue dot).
        * **Processing (STT/Vision):** Busy state (e.g., orange microphone icon, "Processing..." label, or orange dot).
        * **Error (Mic/STT):** Error state (e.g., red microphone icon, "Error" label, or red dot).
    * **`TextInputField` (`QLineEdit`):**
        * Standard text entry: Allows typing and editing of query text.
        * **Placeholder Text:** Displays "Type your query here..." when empty and not focused. Placeholder disappears on focus or when text is entered.
        * **Submission:** Pressing 'Enter' key within this field submits the query (equivalent to clicking `Send/ActivateButton`).
        * **Clearing:** Input is cleared after successful submission.
        * **Focus:**
            * Ideally, the application starts with focus on this field if no introductory elements are present.
            * Focus returns to this field after a query is submitted, allowing for quick follow-up text queries.
    * **`Send/ActivateButton` (`QPushButton`):**
        * **Action:** Clicking this button submits the current content of the `TextInputField`.
        * **State:**
            * Enabled when `TextInputField` contains text.
            * Disabled (grayed out, non-interactive) if `TextInputField` is empty.
            * May briefly show a "Sending..." or busy state if submission involves a slight delay, then returns to normal. For MVP, if processing is quick, this might not be necessary beyond standard pressed feedback.
        * **Visual Feedback:** Standard button hover and pressed states.
        * **Tooltip:** "Send Text Query".

### System State Visual Feedback (Summary)

-   **Application Idle/Ready:** Default UI appearance. `MicrophoneStatusIndicator` is 'Idle'. `TextInputField` is active or ready for input.
-   **Voice Input - Listening:** `MicrophoneStatusIndicator` shows 'Listening' (e.g., blue icon/label).
-   **Voice Input - STT Processing:** `MicrophoneStatusIndicator` shows 'Processing' (e.g., orange icon/label). Transcribed text may appear in `ChatLogWidget`.
-   **Query Processing (Vision Pipeline):**
    * For voice queries, `MicrophoneStatusIndicator` remains 'Processing'.
    * For text queries, the `Send/ActivateButton` might show a brief busy state, or the system relies on the quick appearance of the query in the chat log as acknowledgment.
    * No global intrusive "loading" spinner is planned for MVP to maintain minimalism, assuming processing times are within a few seconds. If longer, this may need reconsideration.
-   **TTS Speaking Response:** No specific visual indicator for "speaking" is active by default beyond the audio output itself. The `MicrophoneStatusIndicator` would have returned to 'Idle' by this point. The textual response is already visible in the `ChatLogWidget`.
-   **Error States:**
    * **Microphone/STT Error:** `MicrophoneStatusIndicator` shows 'Error' (e.g., red icon/label). A message appears in `ChatLogWidget` or as a temporary status notification.
    * **Vision/TTS Error:** Relevant error message appears in `ChatLogWidget`. TTS errors are silent failures primarily, with text still available.
    * **Webcam Error:** Message displayed in `WebcamDisplayWidget`.

---

## Accessibility (AX) Requirements (MVP Focus for PyQt6)

Adherence to basic accessibility principles is important for the Sourcer MVP. Specifications are tailored for a PyQt6 desktop application.

-   **Target Compliance:** While not formally certifying for WCAG, the principles of WCAG 2.1 Level AA will guide design choices, particularly for contrast and keyboard accessibility.

-   **1. Clear Visual Presentation of Text:**
    * **Font Sizing:** Use legible default font sizes as specified in the Mockups section (e.g., 10-11pt for chat, 9pt for status).
    * **Contrast Ratios:**
        * Text-to-background contrast for all UI text (chat messages, button labels, input fields) must meet a minimum of 4.5:1 (WCAG AA).
        * Colors chosen in the "Mockups / Detailed Visual Descriptions" section must be verified using a contrast checker tool.
    * **Information through Color:** Information should not be conveyed by color alone.
        * Example: `MicrophoneStatusIndicator` changes should ideally involve icon changes or textual labels in addition to color, or use very distinct colors that are generally distinguishable.
    * **Text Resizing:**
        * For MVP, the application will rely on OS-level display scaling and font size adjustments.
        * Implementing true in-application dynamic text resizing is a complex feature and deferred post-MVP. Developers should ensure UI elements don't break if system font sizes are moderately increased.

-   **2. Keyboard Navigation:**
    * **Logical Tab Order:** A logical and predictable tab order must be implemented for all interactive elements within the `InputControlWidget`. Suggested order:
        1.  `MicrophoneActivationControl`
        2.  `TextInputField`
        3.  `Send/ActivateButton`
    * **Widget Interaction:**
        * All `QPushButton` elements (`MicrophoneActivationControl`, `Send/ActivateButton`) must be activatable using the `Spacebar` or `Enter` key when they have keyboard focus.
        * `QLineEdit` (`TextInputField`) must support standard keyboard text editing operations.
    * **`ChatLogWidget` (`QTextBrowser` or similar):**
        * When focused, its content area should be scrollable using `Arrow Up/Down`, `Page Up/Down`, `Home/End` keys.
        * Text content within the log should be selectable via keyboard (e.g., Shift + Arrow keys), if supported by the chosen Qt widget.
    * **`WebcamDisplayWidget`:** As a non-interactive display, it does not need to be in the primary tab sequence unless it displays an interactive error message/button.

-   **3. Sufficient Color Contrast:** (Reiterated from Clear Visual Presentation)
    * All UI elements (text, icons, borders that convey information, focus indicators) must have sufficient contrast with their background as per WCAG AA guidelines.
    * The color palette defined in the Mockups section will be the basis, and final color values must be checked.

-   **4. Tooltips for Clarity:**
    * Icon-only buttons (e.g., `MicrophoneActivationControl`, and `Send/ActivateButton` if it uses an icon) must have descriptive tooltips (e.g., "Activate Voice Query", "Send Text Query") that appear on hover. This aids both sighted users and users of assistive technologies if tooltips are exposed.

-   **5. Clear Focus Indicators:**
    * All interactive UI elements that can receive keyboard focus must display a clear visual focus indicator when focused.
    * PyQt's default focus indicators should be used or, if customized (e.g., via stylesheets as described in mockups for `TextInputField`), must be highly visible (e.g., a distinct border or outline).

-   **6. Accessible Naming (for Assistive Technologies):**
    * While full ARIA support is web-centric, ensure standard PyQt widgets have their `accessibleName` and `accessibleDescription` properties set appropriately, especially for controls that are icon-only or have non-obvious functions. This helps screen readers interpret the UI. For many standard widgets like `QPushButton` with text, this is handled automatically.
        * `MicrophoneActivationControl`: Accessible name "Voice Query Button" or similar.
        * `TextInputField`: Accessible name "Query Input" or "Type your query".
        * `Send/ActivateButton`: Accessible name "Send Query Button".

-   **7. Avoid Flashing Content:** No flashing or blinking content will be used, which can be a trigger for seizures. Animations (like subtle pulsing for "processing") should be gentle and not flash rapidly.