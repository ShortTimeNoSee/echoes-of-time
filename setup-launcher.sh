#!/bin/bash

# Detect OS
OS="$(uname -s)"

# Unified setup and play launcher
case "$OS" in
    Linux|Darwin)
        echo "Detected POSIX environment. Running or playing Echoes of Time..."
        
        if [ ! -d "game" ]; then
            echo "Game not found. Running bootstrap.sh to set up..."
            curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/bootstrap.sh | bash
        fi
        
        # After the bootstrap clones the repo, play.sh is inside the 'game' folder.
        if [ -f "game/play.sh" ]; then
            ./game/play.sh
        elif [ -f "play.sh" ]; then
            ./play.sh
        else
            echo "Error: play.sh not found."
            exit 1
        fi
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "Detected Windows environment. Running or playing Echoes of Time..."
        
        if [ ! -d "game" ]; then
            echo "Game not found. Running setup-windows.ps1 to set up..."
            curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-windows.ps1 -o setup-windows.ps1
            powershell -ExecutionPolicy Bypass -File setup-windows.ps1
        fi
        
        if [ -f "game/play.ps1" ]; then
            powershell -ExecutionPolicy Bypass -File game/play.ps1
        else
            echo "Error: play.ps1 not found in game directory."
            # Fallback check for current directory
            if [ -f "play.ps1" ]; then
                 powershell -ExecutionPolicy Bypass -File play.ps1
            fi
        fi
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac
