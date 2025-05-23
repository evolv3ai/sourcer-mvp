# Environment Variables and Configuration

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Environment Variables and Configuration".

For the Sourcer MVP, configuration is primarily managed through a settings file and potentially an example environment file for sensitive or local-override settings, though the local nature of the MVP minimizes the need for complex environment variable management typically seen in web services.

## Configuration File

- **Location:** `config/settings.ini` [cite: 63]
- **Purpose:** To store application settings such as paths to AI models (if not hardcoded or discovered dynamically), default parameters for services, logging levels, etc.
- **Loading:** The application uses `src/sourcer/utils/config_loader.py` to load settings from `settings.ini`.

## Example Environment File

- **Location:** `.env.example`
- **Purpose:** To showcase any environment variables that *could* be used by the application, especially if developers want to override default configurations locally without modifying `settings.ini`. For the MVP, this might be minimal.
- **Usage:** Developers can copy `.env.example` to `.env` and define variables there. The `config_loader.py` or application startup script would need to be adapted to load from `.env` (e.g., using a library like `python-dotenv`).
- **Content:** The `.env.example` would list variables like:
    ```ini
    # .env.example
    # LOG_LEVEL=DEBUG
    # MODEL_BASE_PATH=/custom/path/to/models/
    ```

## Secrets Management

- No external service API keys are needed for MVP core functionality. [cite: 270]
- If any future configuration requires secrets (e.g., optional analytics API key for PostHog), they should **not** be hardcoded or committed to `settings.ini`.
- Such secrets should be managed via an `.env` file (listed in `.gitignore`) or system environment variables, and accessed securely by the application.