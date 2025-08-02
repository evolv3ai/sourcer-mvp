# Sourcer MVP

Sourcer MVP is a locally-running AI webcam application that allows users to understand their immediate visual environment using voice or text queries. All AI processing occurs locally on the user's machine.

## Prerequisites

* Python 3.11.9 [cite: 109, 200]
* `pip` (Python package installer)
* Access to a terminal or command prompt.
* Git (for cloning, though you likely have the project files already).

## Project Structure Overview

The project follows a monorepo structure. Key directories include:
* `src/sourcer/`: Main application Python code. [cite: 65]
* `tests/`: Automated tests. [cite: 70]
* `scripts/`: Utility scripts for development and model management. [cite: 64]
* `config/`: Application configuration files (e.g., `settings.ini`). [cite: 63]
* `models/`: Directory for storing downloaded AI models (this will be populated by a script). [cite: 64]
* `docs/`: Project documentation. [cite: 63]
(For a detailed structure, refer to the Architecture Document, specifically the Project Structure section).

## Development Setup

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd sourcer-mvp
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    ```
    Activate it:
    * Windows: `.\.venv\Scripts\activate`
    * macOS/Linux: `source .venv/bin/activate`

3.  **Install Dependencies:**
    Install development dependencies (includes testing tools, linters, formatters):
    ```bash
    pip install -r requirements-dev.txt 
    ```
    Install runtime dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    ([cite: 71, 217])

4.  **Download AI Models:**
    Run the script to download the necessary AI models. These will be stored in the `models/` directory.
    ```bash
    python scripts/download_models.py
    ```
    ([cite: 64])
    *(Note: Ensure `scripts/download_models.py` is implemented and contains the logic to fetch YOLO, MobileSAM, LLaVA, STT, and TTS models specified in the architecture.)*

5.  **Configure Settings (if necessary):**
    Review `config/settings.ini` [cite: 63] and `.env.example`[cite: 71]. If an `.env` file is used for local overrides, create it from `.env.example` and populate as needed.

## Running the Application for Development

You can run the application using the development script:
```bash
./scripts/run_dev.sh