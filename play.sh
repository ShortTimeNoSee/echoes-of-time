#!/bin/bash

# Navigate to the game directory
cd "$(dirname "$0")/game"

# Detect the OS
OS="$(uname -s)"

# Activate virtual environment and run the game
case "$OS" in
    Linux|Darwin)
        echo "Detected POSIX environment (Linux/macOS)."
        source venv/bin/activate
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "Detected Windows environment."
        source venv/Scripts/activate
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac

# Run the game
echo "Running Echoes of Time..."
python3 game.py
