# setup-windows.ps1
# Unified script to set up the project and install all dependencies automatically on Windows.

# Enable error handling
$ErrorActionPreference = "Stop"

# Function to install Python
function Install-Python {
    Write-Host "Checking for Python installation..."
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        Write-Host "Python3 not found. Installing Python..."
        Invoke-Expression "& winget install -e --id Python.Python.3 --silent"
    } else {
        Write-Host "Python3 is already installed."
    }
}

# Function to install Git
function Install-Git {
    Write-Host "Checking for Git installation..."
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Git not found. Installing Git..."
        Invoke-Expression "& winget install -e --id Git.Git --silent"
    } else {
        Write-Host "Git is already installed."
    }
}

# Function to install curl
function Install-Curl {
    Write-Host "Checking for curl installation..."
    if (-not (Get-Command curl -ErrorAction SilentlyContinue)) {
        Write-Host "curl not found. Installing curl..."
        Invoke-Expression "& winget install -e --id Curl.Curl --silent"
    } else {
        Write-Host "curl is already installed."
    }
}

# Function to check and install dependencies
function Install-Dependencies {
    Install-Python
    Install-Git
    Install-Curl
}

# Clone the repository
function Clone-Repository {
    Write-Host "Cloning the game repository..."
    if (Test-Path "game") {
        Write-Host "Removing existing 'game' directory..."
        Remove-Item -Recurse -Force "game"
    }
    git clone https://github.com/ShortTimeNoSee/echoes-of-time.git game
    Set-Location "game"
}

# Set up virtual environment
function Setup-Venv {
    Write-Host "Setting up a Python virtual environment..."
    python3 -m venv venv
    Write-Host "Activating virtual environment..."
    .\venv\Scripts\Activate.ps1
}

# Install Pygame and run the game
function Install-And-Run-Game {
    Write-Host "Installing Pygame..."
    pip install pygame --quiet
    Write-Host "Running the game..."
    python3 game.py
}

# Main script execution
Write-Host "Starting setup process..."
Install-Dependencies
Clone-Repository
Setup-Venv
Install-And-Run-Game
