# Definitive Tech Stack Selections

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Definitive Tech Stack Selections".

| Category             | Technology              | Version / Details          | Description / Purpose                                  | Justification (Optional)                                                                 |
| :------------------- | :---------------------- | :------------------------- | :----------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| **Languages** | Python                  | 3.11.9                     | Primary language for application logic, AI, UI       | Mandated by project. Good for AI/ML, PyQt bindings.                         | 
| **Runtime** | Python Runtime          | 3.11.9                     | Execution environment for Python code                  | Aligns with language choice.                                                             | 
| **Frameworks** | PyQt6                   | 6.7.0 (example, use latest stable) | Desktop UI framework                                   | Good Python integration, mature, feature-rich for desktop UIs.                           | 
|                      | Pipecat                 | Latest stable (e.g., 0.6.x) | Voice and multimodal AI pipeline orchestration       | Mandated for voice. Simplifies STT/TTS integration.                             | 
| **AI Models** | Ultralytics YOLO        | Latest (e.g., YOLOv8 series) | Local object detection                                 | Mandated. State-of-the-art, good performance.                             | 
|                      | MobileSAM               | Latest compatible          | Local image segmentation (context for LLaVA)         | Mandated. Lightweight SAM variant.                                        | 
|                      | LLaVA                   | Latest compatible          | Local visual language model for descriptions         | Mandated. Good for generating textual scene descriptions.               | 
|                      | Vosk (via Pipecat)      | Latest compatible STT model | Local Speech-to-Text engine                          | Good balance of local performance/accuracy for STT. Integrates with Pipecat.             | 
|                      | Piper TTS (via Pipecat) | Latest compatible TTS model | Local Text-to-Speech engine                          | High-quality local TTS, efficient ONNX models. Integrates with Pipecat.                  | 
| **UI Libraries** | PyQt6                   | 6.7.0 (example)            | Core UI components and layout                          | Chosen framework.                                                                        | 
| **Testing** | Pytest                  | Latest stable (e.g., 8.x.x) | Unit/Integration testing framework                   | Popular, powerful, extensible Python testing framework.                                  | 
|                      | pytest-mock             | Latest stable (e.g., 3.x.x) | Mocking library for Pytest                           | Simplifies mocking within Pytest.                                                        | 
| **CI/CD** | GitHub Actions          | N/A                        | Continuous Integration/Deployment                      | Good integration with GitHub, flexible workflows for build/test/release.                 | 
| **Packaging** | PyInstaller             | Latest stable (e.g., 6.x.x) | Bundles Python app into standalone executable        | Common choice for Python desktop apps, handles dependencies.                             | 
|                      | Inno Setup              | Latest stable (e.g., 6.x.x) | Creates Windows installer package (EXE)              | Powerful and flexible for creating user-friendly Windows installers.                     | 
| **Linters/Formatters**| Black                   | Latest stable (e.g., 24.x.x)| Python code formatter                                  | Uncompromising, ensures consistent code style.                                           | 
|                      | Flake8                  | Latest stable (e.g., 7.x.x) | Python linter (PEP8, pyflakes, McCabe)               | Catches common errors and style issues.                                                  | 
|                      | MyPy                    | Latest stable (e.g., 1.x.x) | Static type checker for Python                       | Enforces type safety, helps catch bugs early.                                            | 
| **Other Tools** | OpenCV-Python           | Latest stable              | Computer vision library (for frame handling)         | Essential for image/video manipulation if needed by webcam or models.                  | 
|                      | NumPy                   | Latest stable              | Numerical Python (for frame data arrays)             | Fundamental package for numerical computation, used for image data.                      | 
|                      | PostHog                 | JS Snippet / Python lib    | User feedback and analytics                          | Specified in PRD for user feedback.                                               | 

*Note: "Latest stable" implies the version available and stable at the time of development commencement. Specific minor/patch versions should be pinned in `requirements.txt`.* [cite: 169]