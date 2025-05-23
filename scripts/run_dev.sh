#!/bin/bash
echo "Starting Sourcer MVP in development mode..."

# Assuming the virtual environment is already activated,
# or Python 3.11 is the default system Python.
# Add virtual environment activation if a standard venv path is established, e.g.:
# SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
# VENV_PATH="$SCRIPT_DIR/../.venv" # Example path
# if [ -d "$VENV_PATH" ]; then
# source "$VENV_PATH/bin/activate"
# else
# echo "Warning: Virtual environment not found at $VENV_PATH. Using system Python."
# fi

python src/sourcer/main.py

echo "Sourcer MVP exited."
