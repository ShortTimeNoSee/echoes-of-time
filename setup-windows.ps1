#!/bin/bash

set -e

# Detect OS and Shell
OS="$(uname -s)"
SHELL_TYPE="$(ps -p $$ -o comm=)"
echo "Detected OS: $OS"
echo "Detected Shell: $SHELL_TYPE"

# Handle macOS/Linux
if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    echo "Running macOS/Linux setup..."
    curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-posix.sh | bash
    exit 0
fi

# Handle Windows
if [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* || "$OS" == "MSYS_NT"* ]]; then
    echo "Detected Windows..."
    if [[ "$SHELL_TYPE" =~ "powershell" || "$SHELL_TYPE" =~ "cmd" ]]; then
        echo "Running PowerShell/Command Prompt setup..."
        curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-windows.ps1 | powershell -Command -
    else
        echo "Running Git Bash setup..."
        curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-posix.sh | bash
    fi
    exit 0
fi

# Unsupported OS
echo "Unsupported OS or Shell. Please install manually."
exit 1
