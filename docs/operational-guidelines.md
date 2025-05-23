# Operational Guidelines

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Operational Guidelines including Coding Standards, Testing, Error Handling, and Security".

## Error Handling Strategy [cite: 177]

  - **General Approach:** Use Python's standard exception handling (`try-except` blocks). Define custom exception classes inheriting from a base `SourcerException` for application-specific errors.
  - **Logging:** [cite: 179]
      - Library/Method: Python's built-in `logging` module.
      - Format: Plain text with timestamp, log level, module name, and message. E.g., `YYYY-MM-DD HH:MM:SS - LEVEL - module_name - Message`. JSON format could be considered if advanced log analysis becomes necessary.
      - Levels: [cite: 182]
          - `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
          - `INFO`: Confirmation that things are working as expected (e.g., application start, model loaded).
          - `WARNING`: An indication that something unexpected happened, or an indication of some problem in the near future (e.g., 'disk space low'). The software is still working as expected.
          - `ERROR`: Due to a more serious problem, the software has not been able to perform some function (e.g., model failed to load, webcam access denied). [cite: 186]
          - `CRITICAL`: A serious error, indicating that the program itself may be unable to continue running. [cite: 187]
      - Context: Include function name, relevant parameters (sanitized if sensitive) where helpful for debugging. No PII in logs.
  - **Specific Handling Patterns:** [cite: 188]
      - **AI Model Errors:** (e.g., model loading failure, inference error) [cite: 188]
          - Log the detailed error.
          - Display a user-friendly message in the UI (e.g., "Visual analysis failed. Please try again.").
          - Gracefully degrade if possible (e.g., if one model in a chain fails, indicate partial results or failure).
      - **Webcam Errors:** (e.g., not found, access denied) [cite: 191]
          - Log the error.
          - Display a clear message in the UI (e.g., "Webcam not detected or access denied. Please check your webcam settings.").
          - Disable functionality dependent on the webcam. [cite: 193]
      - **Pipecat/STT/TTS Errors:** [cite: 193]
          - Log errors from Pipecat services.
          - UI feedback (e.g., "Speech recognition failed," "Could not play audio response.").
      - **File/Resource Errors:** (e.g., config file not found) [cite: 195]
          - Log the error.
          - Display a user-friendly message. [cite: 196]
          - Application might fail to start if critical resources are missing.
      - **User Input Validation:** (Though minimal for MVP queries) [cite: 197]
          - If text input has constraints in the future, validate and provide immediate feedback.
      - **Unhandled Exceptions:** Implement a global exception hook (e.g., `sys.excepthook`) to catch any unhandled exceptions, log them, and display a generic error message to the user ("An unexpected error occurred. Please restart Sourcer.") before attempting a graceful shutdown or exit.

## Coding Standards [cite: 199]

These standards are mandatory for all code generation by AI agents and human developers.
  - **Primary Runtime(s):** Python 3.11.9 [cite: 200]
  - **Style Guide & Linter:** [cite: 200]
      - Formatter: `Black` (default configuration). Run on save / pre-commit. [cite: 201]
      - Linter: `Flake8` with plugins (`flake8-bugbear`, `flake8-comprehensions`, `flake8-print`). Configuration in `pyproject.toml` or `.flake8`.
      - Type Checker: `MyPy` (run in CI, strive for strictness). Configuration in `pyproject.toml`.
      - Linter rules are mandatory and must not be disabled without cause documented in comments.
  - **Naming Conventions:** [cite: 204]
      - Variables: `snake_case` [cite: 204]
      - Functions/Methods: `snake_case` [cite: 204]
      - Classes/Types/Interfaces: `PascalCase` [cite: 204]
      - Constants: `UPPER_SNAKE_CASE` [cite: 204]
      - Files: `snake_case.py` [cite: 204]
      - Modules/Packages: `snake_case` [cite: 205]
  - **File Structure:** Adhere to the layout defined in the "Project Structure" section. [cite: 205]
  - **Unit Test File Organization:** Unit tests will be located in the `tests/unit/` directory, mirroring the structure of the `src/sourcer/` package. For example, tests for `src/sourcer/core/orchestrator.py` will be in `tests/unit/core/test_orchestrator.py`. [cite: 206]
      - **Unit Test File Naming Convention:** Test files will be named `test_*.py`. Test methods/functions within these files will be prefixed with `test_`.
  - **Asynchronous Operations:** While Pipecat handles async operations for voice, core application logic interacting with it should use appropriate async patterns if Pipecat's client library is async. For PyQt, ensure long-running tasks are offloaded from the main UI thread to prevent freezing (e.g., using `QThread` or `QtConcurrent`).
  - **Type Safety:** [cite: 210]
      - All new Python code must include type hints.
      - `MyPy` will be used for static type checking, with `disallow_untyped_defs = True` as a goal.
      - *Type Definitions:* Co-located with usage or in dedicated `types.py` files within modules if complex/shared. Avoid `typing.Any` where specific types can be used. [cite: 213]
  - **Comments & Documentation:** [cite: 213]
      - Code Comments: Explain *why*, not *what*, for complex logic. Use Google Python Style Docstrings for modules, classes, functions, and methods.
      - READMEs: The main `README.md` will cover project setup and usage. Complex modules may have their own READMEs if necessary.
  - **Dependency Management:** [cite: 216]
      - Tool: `pip` with `requirements.txt` (for runtime) and `requirements-dev.txt` (for development).
      - Policy: Pin exact versions (e.g., `library==1.2.3`) to ensure reproducible builds. Adding new dependencies requires a brief justification and check for existing alternatives or security vulnerabilities.

### Detailed Language & Framework Conventions [cite: 219]

#### Python Specifics: [cite: 219]

  - **Immutability:** Prefer immutable data structures where practical (e.g., tuples instead of lists for fixed collections). For classes, consider `@dataclass(frozen=True)` if appropriate. Be mindful of mutable default arguments in function definitions.
  - **Functional vs. OOP:** Employ classes for representing entities (data models), UI components (PyQt), and services with state or complex behavior. Use functions for stateless operations and utility tasks. List comprehensions and generator expressions are preferred over `map`/`filter` functions for readability when simple.
  - **Error Handling Specifics:** Always raise specific, custom exceptions inheriting from a base `SourcerException` (e.g., `ModelLoadError`, `VisionProcessingError`). Use `try-except-else-finally` blocks appropriately. Avoid broad `except Exception:` clauses without re-raising or specific, justified handling.
  - **Resource Management:** Always use `with` statements for resources that need to be managed (e.g., file operations, though less critical for this MVP's core). Pipecat and PyQt manage their own resources internally to a large extent.
  - **Type Hinting:** All new functions and methods must have full type hints. Run MyPy in CI. Aim for `disallow_untyped_defs = True` in `mypy.ini` or `pyproject.toml`. [cite: 228]
  - **Logging Specifics:** Use the `logging` module. Configure a basic formatter providing timestamp, level, module, and message. Do not log sensitive PII. Use appropriate log levels.
  - **Code Generation Anti-Patterns to Avoid:** Avoid overly nested conditional logic (max 2-3 levels if possible, refactor otherwise). Avoid single-letter variable names unless for trivial loop counters (e.g., `i`, `j`, `k`) or conventional mathematical notation. Avoid "magic numbers"; use named constants. [cite: 232]

#### PyQt Specifics: [cite: 232]

  - **Threading:** Perform long-running operations (like AI model inference if it blocks, or complex I/O) in separate `QThread`s to keep the UI responsive. Use signals and slots for communication between threads and the main UI thread.
  - **Signal/Slot Mechanism:** Use Qt's signal and slot mechanism for communication between UI components and between UI and backend logic. This promotes loose coupling. [cite: 235]
  - **UI Design:** While detailed UI design is for a Design Architect, ensure UI code is well-organized. Separate UI widget definitions from application logic where possible. Consider using Qt Designer (`.ui` files) and `uic.loadUi` for more complex UIs if preferred, or define UIs purely in Python. For MVP, Python-defined UI is likely sufficient. [cite: 237]
  - **Resource Management:** PyQt objects (especially `QWidget` descendants) are often managed in a parent-child hierarchy. Ensure proper parenting to manage object lifetimes. [cite: 238]
  - **Styling:** Use Qt Style Sheets for basic UI styling if needed, rather than hardcoding visual properties extensively.

## Overall Testing Strategy [cite: 239]

  - **Tools:** `pytest` for test running and structure, `pytest-mock` for mocking.
  - **Unit Tests:** [cite: 240]
      - **Scope:** Test individual functions, methods, and classes in isolation. Focus on business logic within orchestrator, service wrappers, utility functions, and individual UI component logic (if separable).
      - **Location:** `tests/unit/` mirroring `src/sourcer/` structure. E.g., `tests/unit/core/test_orchestrator.py`. [cite: 242]
      - **Naming:** Test files `test_*.py`, test functions `test_*()`.
      - **Mocking/Stubbing:** Use `pytest-mock` (which wraps `unittest.mock`). Mock external dependencies such as Pipecat client calls, direct AI model library calls (if not fully wrapped by services), file system access, and time (if time-sensitive logic exists). For AI models, mock their `predict` or `process` methods to return predefined outputs.
      - **AI Agent Responsibility:** The AI Agent must generate unit tests covering all public methods of new/modified classes, significant logic paths, common input variations, edge cases, and error conditions.
  - **Integration Tests:** [cite: 246]
      - **Scope:** Test the interaction between several components. E.g.: [cite: 247]
          - `CoreOrchestrator` with mocked `VisionService`, `STTService`, `TTSService` to verify overall flow.
          - `VisionService` with mocked individual model wrappers (YOLO, SAM, LLaVA) to test their internal orchestration.
          - UI components with mocked backend services to test signal/slot connections and basic UI updates (might be limited without full UI automation).
      - **Location:** `tests/integration/`. [cite: 250]
      - **Environment:** Run locally. Use mocked versions of heavy components like full AI models or Pipecat. Testcontainers are overkill for this local desktop app. [cite: 251]
      - **AI Agent Responsibility:** May be tasked with generating integration tests for key interaction points between major services.
  - **End-to-End (E2E) Tests:** [cite: 252]
      - **Scope:** Manual for MVP. Testers will follow scripts covering primary user flows: voice query for common object, text query, ensuring correct visual/audio/textual response within performance targets.
      - **Tools:** N/A for automated E2E in MVP. [cite: 254]
      - **AI Agent Responsibility:** N/A for MVP automated E2E.
  - **Test Coverage:** [cite: 255]
      - **Target:** Aim for >80% line coverage for unit tests on critical business logic. Focus on test quality over raw numbers. [cite: 256]
      - **Measurement:** `pytest-cov` plugin for `pytest` (generates coverage reports).
  - **Mocking/Stubbing Strategy (General):** Prefer focused mocks on direct dependencies. Avoid mocking transitive dependencies unless absolutely necessary. Strive for tests that are fast, reliable, and easy to understand.
  - **Test Data Management:** For unit/integration tests, define test data (e.g., sample frame data as numpy arrays, sample query strings, expected description texts) directly within test files or in small, co-located helper files/fixtures.
  - **CLI Testability:** Core processing elements should be testable via CLI. The `VisionService` (or its underlying model wrappers) should allow analysis of a saved image file via a simple script in `scripts/`. This aids debugging and component verification outside the full UI.

## Security Best Practices [cite: 263]

  - **Input Sanitization/Validation:** [cite: 263]
      - User typed input (queries): For MVP, queries are relatively free-form. Future features requiring structured input must validate it. [cite: 264]
      - No external API calls means reduced attack surface from malicious external data.
      - File paths (e.g., for models in config): Validate paths to prevent directory traversal if paths become user-configurable. For MVP, these are likely fixed or internally derived. [cite: 266]
  - **Output Encoding:** [cite: 266]
      - Text displayed in PyQt UI: PyQt widgets generally handle text rendering safely. Avoid constructing HTML or rich text manually with unvalidated user/AI-generated content if such features were added.
      - Spoken output: TTS engines process plain text; risk of injection into the TTS voice itself is low with reputable local engines.
  - **Secrets Management:** [cite: 269]
      - No external service API keys are needed for MVP core functionality.
      - If any future configuration requires secrets (e.g., optional analytics API key), they should not be hardcoded. Use environment variables or a secure config mechanism, and ensure they are not committed to the repository (e.g., via `.env` files listed in `.gitignore`).
  - **Dependency Security:** [cite: 272]
      - Regularly update dependencies in `requirements.txt` and `requirements-dev.txt`.
      - Use tools like `pip-audit` or GitHub's Dependabot alerts to check for known vulnerabilities in dependencies. Address critical/high vulnerabilities promptly.
  - **Local Data Privacy:** The core design principle is local processing. Ensure no accidental data leakage: [cite: 275]
      - Webcam feed, audio input, and generated descriptions must strictly remain on the local device.
      - Verify that none of the integrated libraries (Pipecat, AI models) make unauthorized network calls with user data. This can be checked during development with network monitoring tools.
  - **Code Integrity:** [cite: 278]
      - Ensure model files downloaded are from official/trusted sources and ideally have checksums for verification if provided by the model distributors.
  - **Principle of Least Privilege (Application Context):** [cite: 279]
      - The application should only request permissions it absolutely needs (e.g., webcam, microphone).
      - File system access should be limited to necessary directories (e.g., model storage, configuration).
  - **Error Handling & Information Disclosure:** [cite: 281]
      - User-facing error messages should be generic and not reveal internal application structure, stack traces, or sensitive paths. Log detailed errors internally for debugging. [cite: 282]
  - **Installation Package Security:** [cite: 282]
      - Ensure the installer created by Inno Setup doesn't bundle unnecessary executables or create insecure system configurations.
      - If code signing becomes an option (post-MVP, as it involves costs/certificates), it would enhance trust.