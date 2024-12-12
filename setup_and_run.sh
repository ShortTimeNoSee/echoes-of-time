#!/bin/bash

echo "Cloning repository..."
git clone https://github.com/ShortTimeNoSee/echoes-of-time game 
cd game

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing via Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
fi

echo "Installing Pygame..."
pip3 install pygame

echo "Running the game..."
python3 game.py
