import sys
import os

# Add script directory to Python PATH to ensure imports work correctly when called from elsewhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puml_cli.cli import main

if __name__ == "__main__":
    main()
