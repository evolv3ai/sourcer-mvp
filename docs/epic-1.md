# Epic 1: Application Shell and Visual Foundation

> This document is a granulated shard from the main "Sourcer Product Requirements Document (PRD)" focusing on "Epic 1: Application Shell and Visual Foundation".

- **Goal:** Establish the foundational project structure, core configurations, and the basic application shell, including webcam feed display and UI placeholders for interactions.
- **Story 0: Setup Initial Project Structure and Core Configuration**
    - Goal: To establish the foundational directory structure, version control, and core configuration files for the project, enabling subsequent development activities.
    - As a Developer, I want the initial project scaffold created as per the Architecture Document, including version control initialization and basic configuration files, so that I have the correct and consistent workspace to start building the application features.
    - Acceptance Criteria:
        1.  The main project directory (e.g., `sourcer-mvp/`) is created and initialized as a Git repository.
        2.  A standard `.gitignore` file suitable for Python projects is present.
        3.  Core subdirectories (`src/sourcer`, `tests/unit`, `tests/integration`, `scripts`, `config`, `assets/icons`, `docs`, `.github/workflows`) are created as defined in the Architecture Document's Project Structure section.
        4.  Initial essential Python package files (e.g., `src/sourcer/__init__.py`, `src/sourcer/core/__init__.py`, etc.) are created to define the package structure.
        5.  Stub files for main application entry points (`src/sourcer/app.py`, `src/sourcer/main.py`) are created.
        6.  Initial dependency files (`requirements.txt`, `requirements-dev.txt`) are created, listing at least the linters/formatters/testing tools from the tech stack.
        7.  A `pyproject.toml` file is created with basic configurations for Black, Flake8, and MyPy.
        8.  A stub configuration file (`config/settings.ini`) and an example environment file (`.env.example`) are present as per the architecture.
        9.  A basic GitHub Actions workflow file (e.g., `main.yml`) is created in `.github/workflows/` that triggers on push/PR to `main` and runs linters, type checkers, and unit tests.
- **Story 1: As an AI Enthusiast, I want to install (from the prepared environment) and launch the Sourcer application so that I can see the main interface.**
    - Acceptance Criteria:
        - Application installs successfully into the development environment using `pip install -r requirements.txt` (and dev dependencies).
        - Application launches via `scripts/run_dev.sh` or `python src/sourcer/main.py` and displays a main window.
        - A designated area for webcam feed is present.
        - A designated area for chat/log history is present. [cite: 501]
        - A text input field is present.
- **Story 2: As an AI Enthusiast, I want to see a live feed from my default webcam within the application so that I know what the application is "seeing".**
    - Acceptance Criteria:
        - Application automatically detects and uses the default system webcam.
        - Live video from the webcam is displayed clearly in the designated UI area. [cite: 504]
        - Video feed is reasonably smooth (e.g., >10 FPS, architect to define target).
        - Notes for Architect/Scrum Master: Consider graceful handling if no webcam is found or access is denied. [cite: 506]