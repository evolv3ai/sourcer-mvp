#!/bin/bash
# Development runner script for Sourcer MVP

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Sourcer MVP in development mode...${NC}"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv "$PROJECT_ROOT/.venv"
fi

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Check if dependencies are installed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not installed. Installing...${NC}"
    pip install -r "$PROJECT_ROOT/requirements-python312.txt"
fi

# Set environment variables for development
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"
export DEBUG=true
export LOG_LEVEL=DEBUG
export QT_QPA_PLATFORM=offscreen  # For WSL compatibility

# Check if models directory has content
if [ ! "$(ls -A $PROJECT_ROOT/models 2>/dev/null)" ]; then
    echo -e "${YELLOW}Models directory is empty. Run 'python scripts/download_models.py' to download models.${NC}"
fi

# Run the application
echo -e "${GREEN}Launching Sourcer...${NC}"
cd "$PROJECT_ROOT"
python3 src/sourcer/main.py "$@"