# Sourcer MVP

Sourcer MVP is a locally-running AI webcam application that allows users to understand their immediate visual environment using voice or text queries. All AI processing occurs locally on the user's machine.

## Features

- Live webcam feed display
- Voice input (Speech-to-Text) using Vosk
- Visual analysis using YOLO, MobileSAM, and LLaVA
- Voice output (Text-to-Speech) using Piper
- Completely local processing for privacy
- Cross-platform desktop application using PyQt6

## Prerequisites

- Python 3.11.9
- Webcam
- Microphone (for voice input)
- 8GB+ RAM recommended
- GPU recommended for better performance

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd sourcer
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download AI models:
```bash
python scripts/download_models.py
```

5. Run the application:
```bash
./scripts/run_dev.sh  # On Windows: python src/sourcer/main.py
```

## Development

For development setup with linting and testing tools:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```

Run linters:
```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Documentation

See the `docs/` directory for detailed documentation including:
- Architecture overview
- API reference
- Component documentation
- Deployment guides

## License

[License information to be added]