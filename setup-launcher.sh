#!/bin/bash

# Detect OS
OS="$(uname -s)"

case "$OS" in
    Linux|Darwin)
        # POSIX-compatible environments
        echo "Detected POSIX environment. Running bootstrap.sh..."
        curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/bootstrap.sh | bash
        ;;
    CYGWIN*|MINGW*|MSYS*)
        # Windows
        echo "Detected Windows environment. Running setup-windows.ps1..."
        curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-windows.ps1 -o setup-windows.ps1
        powershell -ExecutionPolicy Bypass -File setup-windows.ps1
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac
