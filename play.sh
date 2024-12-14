#!/bin/bash

# Navigate to game directory
cd "$(dirname "$0")/game"

# Activate virtual environment
source venv/bin/activate

# Run the game
python3 game.py
