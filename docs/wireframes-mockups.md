## Wireframes & Mockups

This section describes conceptual wireframes for the Sourcer MVP's main application window and its key components. These descriptions aim to guide the layout and visual structure, which should be implemented using PyQt6, adhering to a clean, functional, and modern minimalist aesthetic.

### Conceptual Wireframe: Main Application Window (`MainWindow`)

-   **Overall Layout:** The `MainWindow` will adopt a primary two-pane or a three-section vertical layout. The goal is to provide an intuitive arrangement of information and controls.
    * **Option A (2-Pane Vertical Split):**
        * **Left Pane (Dominant):** `WebcamDisplayWidget` (approx. 60-70% of window width).
        * **Right Pane:** `ChatLogWidget` stacked above `InputControlWidget` (approx. 30-40% of window width).
    * **Option B (3-Section Vertical Stack):**
        * **Top Section (Dominant):** `WebcamDisplayWidget` (approx. 50-60% of window height).
        * **Middle Section:** `ChatLogWidget` (approx. 30-35% of window height).
        * **Bottom Section (Compact):** `InputControlWidget` (approx. 10-15% of window height).
    * *(User/Stakeholder input requested to select preferred layout. For now, Option B will be assumed for further descriptions due to typical desktop application layouts.)*

-   **Window Properties:**
    * Standard title bar displaying "Sourcer MVP" and an application icon (if provided in `assets/`).
    * Standard window controls (minimize, maximize, close).
    * The window should be resizable, with components adjusting their size proportionally or as defined (e.g., input area fixed height, others flexible). Minimum sensible window size should be considered during development.

### Conceptual Wireframe Detail: `WebcamDisplayWidget`

-   **Location:** Top section of the `MainWindow` (assuming Layout Option B).
-   **Appearance:**
    * A clearly demarcated rectangular area.
    * Displays the live video feed from the system's default webcam.
    * A simple border to visually contain the feed.
-   **Content/Feedback:**
    * If the webcam is active, the live feed is shown.
    * **Error State:** If the webcam is not detected, disconnected, or permissions are denied, this area should display a clear message (e.g., "Webcam not available" or "Webcam access denied") overlaid on a static background or placeholder image (e.g., a generic webcam icon). The message should be centered and easily readable.

### Conceptual Wireframe Detail: `ChatLogWidget`

-   **Location:** Middle section of the `MainWindow`, below the `WebcamDisplayWidget`.
-   **Appearance:**
    * A scrollable area to display the history of interactions.
    * A vertical scrollbar should appear automatically when content exceeds the visible area.
    * Each interaction (user query or system response) will be a distinct entry.
-   **Content/Feedback:**
    * **User Queries:** Clearly labeled (e.g., prefixed with "You: " or an icon). Text aligned to one side (e.g., right).
    * **System Responses:** Clearly labeled (e.g., prefixed with "Sourcer: " or a bot icon). Text aligned to the opposite side (e.g., left).
    * Timestamps for messages are a potential future enhancement but are out of scope for the MVP to maintain simplicity.
    * The most recent messages should be visible, with the view automatically scrolling to the bottom when new messages are added.

### Conceptual Wireframe Detail: `InputControlWidget`

-   **Location:** Bottom, compact section of the `MainWindow`.
-   **Appearance:**
    * A horizontal arrangement of input elements.
    * The area should have a clear visual separation from the `ChatLogWidget` above it (e.g., a thin line or slight background differentiation).
-   **Components (arranged horizontally, left to right typically):**
    1.  **`MicrophoneActivationControl`:**
        * A button, primarily icon-based (e.g., a microphone symbol).
        * Tooltip: "Activate Voice Query" or "Hold to Talk" / "Click to Ask" depending on interaction model.
    2.  **`MicrophoneStatusIndicator`:** (This might be integrated into the `MicrophoneActivationControl` itself via icon changes, or be a small distinct element next to it.)
        * A small visual cue (e.g., a colored dot, a changing icon, or a short text label like "Listening", "Processing").
    3.  **`TextInputField`:**
        * A standard single-line text input box.
        * Placeholder text: e.g., "Type your query here..."
        * Should occupy the majority of the width of the `InputControlWidget`.
    4.  **`Send/ActivateButton`:**
        * A button to submit the text query.
        * Can be text-based ("Send") or icon-based (e.g., paper airplane, right arrow).
        * Tooltip: "Send Text Query".

---

### Mockups / Detailed Visual Descriptions (Minimalist PyQt6 Implementation)

This section translates the wireframes into a visual design aligned with a "clean, functional, and modern minimalist" aesthetic, achievable with PyQt6. A light theme is assumed as a baseline.

-   **Overall Theme:**
    * **Primary Background:** Light gray (e.g., `#F0F0F0` or Qt's default window background).
    * **Window Title Bar:** Standard OS-provided title bar.

-   **Color Palette (Conceptual - actual values to be chosen for good contrast):**
    * **Main Background:** `#F5F5F5` (Very light gray)
    * **Chat Log/Input Area Background:** `#FFFFFF` (White) or a slightly off-white like `#FAFAFA` to differentiate from the main background if needed, or keep same as main for ultra-minimalism.
    * **Text Color (Primary):** `#333333` (Dark Gray) for general text.
    * **Text Color (Secondary/Placeholders):** `#777777` (Medium Gray).
    * **Accent Color (Buttons, Focus, Active States):** A calm, desaturated Blue (e.g., `#4A90E2`) or Teal (e.g., `#50E3C2`).
    * **Microphone Status Colors:**
        * Idle: `#777777` (Medium Gray icon).
        * Listening: Accent Blue/Teal (e.g., `#4A90E2` icon or ring).
        * Processing: A calm Orange/Amber (e.g., `#F5A623`).
        * Error: A muted Red (e.g., `#D0021B`).
    * **Borders/Dividers:** Very light gray (`#DDDDDD`) or omitted if spacing is sufficient.

-   **Typography:**
    * **Font Family:** Leverage system default sans-serif fonts (PyQt's default behavior usually handles this well, ensuring a native feel). E.g., Segoe UI on Windows.
    * **Font Sizes:**
        * `ChatLogWidget` messages: e.g., 10pt or 11pt.
        * `TextInputField`: e.g., 10pt.
        * Status messages/labels: e.g., 9pt.
    * **Font Weights:** Regular for body text. Medium or Semibold for labels like "You:" or "Sourcer:" if needed for emphasis, but can be achieved with color/alignment too.

-   **Iconography:**
    * Use simple, clean, line-style icons. Qt's `QStyle.standardIcon` can provide some system-themed icons (e.g., for error states if applicable).
    * For custom icons (microphone, send): SVG format is preferred for scalability if not using standard Qt icons. Ensure they match the minimalist aesthetic.
        * Microphone Icon: Simple outline.
        * Send Icon: Paper airplane outline.

-   **Spacing & Grid (Conceptual):**
    * Consistent padding within components (e.g., 8-12px).
    * Clear spacing between major UI areas (e.g., 10-15px).
    * Elements within `InputControlWidget` should be vertically centered and have consistent horizontal spacing.

-   **Specific Widget Styling (PyQt Feasible using StyleSheets):**
    * **`WebcamDisplayWidget`:**
        * A thin, solid border (e.g., 1px `#DDDDDD`).
        * Error message text: Centered, primary text color, on the main background if feed fails.
    * **`ChatLogWidget`:**
        * No border for the widget itself if background is differentiated.
        * **User Message Bubbles/Entries:** Background `accent_color_light` (e.g., very light blue `#E7F0FE` if accent is blue) or just different alignment (right-aligned). Text: primary text color.
        * **Sourcer Message Bubbles/Entries:** Background `secondary_background_chat` (e.g., `#ECECEC` if light theme). Text: primary text color. Left-aligned.
        * Rounded corners for message entries/bubbles can be achieved with `border-radius` in Qt StyleSheets for a softer, modern look.
        * Scrollbar: Standard system scrollbar, or styled minimally if possible (often tricky to get cross-platform consistency with heavy scrollbar styling).
    * **`InputControlWidget`:**
        * Slightly different background from chat log if needed for separation, or a top border.
        * **`MicrophoneActivationControl` (Button):**
            * Flat style: `background-color: transparent; border: none;`
            * Icon color changes based on microphone status (see Color Palette).
            * Hover/Pressed states: Subtle background highlight (e.g., light gray) or icon color change.
            * Padding around icon to ensure adequate click target.
        * **`MicrophoneStatusIndicator`:**
            * If a separate dot: Small circle (e.g., 8-10px diameter) filled with status color.
            * If a text label: Short, clear, e.g., "Listening...", "Processing...", "Error". Color changes with status.
        * **`TextInputField` (`QLineEdit`):**
            * Clean, flat appearance. `border: 1px solid #CCCCCC; border-radius: 4px; padding: 5px; background-color: #FFFFFF;`
            * Focus state: Border changes to `accent_color`.
            * Placeholder text color: `secondary_text_color`.
        * **`Send/ActivateButton` (`QPushButton`):**
            * Flat style: `background-color: accent_color; color: white; border: none; border-radius: 4px; padding: 5px 10px;`
            * Icon if used: White, to contrast with accent background.
            * Hover state: Slightly darker accent color.
            * Pressed state: Slightly darker again or inset look.
            * Disabled state (if used during processing): Muted background and text color.

-   **Cleanliness & Minimalism:**
    * Avoid gradients, excessive shadows, or overly ornate decorations.
    * Focus is on content, clear hierarchy, and ease of interaction.
    * Generous use of white space (or light space) to prevent clutter.
    * Visual feedback should be clear but not distracting.