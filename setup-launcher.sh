#!/bin/bash

# Detect OS
OS="$(uname -s)"

# Unified setup and play launcher
case "$OS" in
    Linux|Darwin)
        echo "Detected POSIX environment. Running or playing Echoes of Time..."
        cd "$(dirname "$0")"
        if [ ! -d "game" ]; then
            echo "Game not found. Running bootstrap.sh to set up..."
            curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/bootstrap.sh | bash
        fi
        ./play.sh
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "Detected Windows environment. Running or playing Echoes of Time..."
        if (-not (Test-Path "game")) {
            Write-Host "Game not found. Running setup-windows.ps1 to set up..."
            curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-windows.ps1 -o setup-windows.ps1
            powershell -ExecutionPolicy Bypass -File setup-windows.ps1
        }
        ./play.ps1
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac
