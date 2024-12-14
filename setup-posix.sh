#!/bin/bash

set -e

# Install Python if not found
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing Python..."
    if [[ "$(uname -s)" == "Darwin" ]]; then
        # macOS: Install Homebrew and Python
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    elif [[ "$(uname -s)" == "Linux" ]]; then
        # Linux: Install Python using apt-get
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip
        else
            echo "Package manager not detected. Please install Python manually."
            exit 1
        fi
    fi
fi

# Clone repository and set up
echo "Cloning the game repository..."
if [ -d "game" ]; then
    rm -rf game
fi
git clone https://github.com/ShortTimeNoSee/echoes-of-time.git game
cd game

# Set up virtual environment
echo "Setting up a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Pygame
echo "Installing Pygame..."
pip install pygame

# Run the game
echo "Running the game..."
python3 game.py
