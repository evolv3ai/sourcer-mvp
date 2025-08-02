#!/usr/bin/env python3
"""Main entry point for Sourcer MVP."""

import sys
import traceback
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sourcer.app import create_app


def main() -> int:
    """Main function to run the Sourcer application."""
    try:
        app = create_app()
        exit_code = app.run()
        app.cleanup()
        return exit_code
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())