#!/bin/bash

set -e

# Detect OS
OS="$(uname -s)"
SHELL_TYPE="$(ps -p $$ -o comm=)"
echo "Detected OS: $OS"
echo "Detected Shell: $SHELL_TYPE"

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
    elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS_NT"* ]]; then
        if command -v winget &> /dev/null; then
            winget install -e --id Python.Python.3
        else
            echo "winget not found. Install Python manually from https://www.python.org/"
            exit 1
        fi
    else
        echo "Unsupported OS for Python installation."
        exit 1
    fi
}

# Function to install Git
install_git() {
    echo "Installing Git..."
    if [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
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
    elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS_NT"* ]]; then
        if command -v winget &> /dev/null; then
            winget install -e --id Git.Git
        else
            echo "winget not found. Install Git manually from https://git-scm.com/"
            exit 1
        fi
    else
        echo "Unsupported OS for Git installation."
        exit 1
    fi
}

# Function to install curl
install_curl() {
    echo "Installing curl..."
    if [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
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
    elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS_NT"* ]]; then
        if command -v winget &> /dev/null; then
            winget install -e --id Curl.Curl
        else
            echo "winget not found. Install curl manually."
            exit 1
        fi
    else
        echo "Unsupported OS for curl installation."
        exit 1
    fi
}

# Check and install dependencies
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

if [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS_NT"* ]]; then
    # Activate virtual environment for Windows
    source venv/Scripts/activate
else
    # Activate virtual environment for macOS/Linux
    source venv/bin/activate
fi

# Install Pygame
echo "Installing Pygame..."
pip install pygame

# Run the game
echo "Running the game..."
python3 game.py
