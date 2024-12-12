#!/bin/bash

set -e

# Detect platform
OS="$(uname -s)"
echo "Detected OS: $OS"

# Install Python if not found
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing Python..."
    if [ "$OS" == "Darwin" ]; then
        # macOS: Install Homebrew and Python
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    elif [[ "$OS" == "Linux" || "$OS" == "CYGWIN"* || "$OS" == "MINGW"* ]]; then
        # Windows with WSL or native Linux
        echo "Installing Python for Linux/Windows..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip
        elif command -v winget &> /dev/null; then
            winget install -e --id Python.Python.3
        else
            echo "Package manager not detected. Please install Python manually."
            exit 1
        fi
    else
        echo "Unsupported OS. Please install Python manually."
        exit 1
    fi
fi

# Clone the repository
echo "Cloning the game repository..."
if [ -d "game" ]; then
    rm -rf game
fi
git clone https://github.com/ShortTimeNoSee/echoes-of-time.git game
cd game

# Install Pygame
echo "Installing Pygame..."
pip3 install pygame

# Run the game
echo "Running the game..."
python3 game.py
