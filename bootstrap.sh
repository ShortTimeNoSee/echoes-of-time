#!/bin/bash

set -e

# Detect OS
OS="$(uname -s)"
echo "Detected OS: $OS"

# Function to install Python
install_python() {
    echo "Installing Python..."
    if [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    elif [[ "$OS" == "Linux" ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        else
            echo "No supported package manager found. Install Python manually."
            exit 1
        fi
    fi
}

# Function to install Git
install_git() {
    echo "Installing Git..."
    if [[ "$OS" == "Darwin" ]]; then
        brew install git
    elif [[ "$OS" == "Linux" ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y git
        elif command -v yum &> /dev/null; then
            sudo yum install -y git
        else
            echo "No supported package manager found. Install Git manually."
            exit 1
        fi
    fi
}

# Function to install curl
install_curl() {
    echo "Installing curl..."
    if [[ "$OS" == "Darwin" ]]; then
        brew install curl
    elif [[ "$OS" == "Linux" ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y curl
        elif command -v yum &> /dev/null; then
            sudo yum install -y curl
        else
            echo "No supported package manager found. Install curl manually."
            exit 1
        fi
    fi
}

# Install dependencies
if ! command -v python3 &> /dev/null; then
    install_python
fi

if ! command -v git &> /dev/null; then
    install_git
fi

if ! command -v curl &> /dev/null; then
    install_curl
fi

# Clone the repository
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
