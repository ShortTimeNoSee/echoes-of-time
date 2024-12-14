# setup-windows.ps1
# Automatic setup for Windows environments

# Enable error handling
$ErrorActionPreference = "Stop"

# Function to install Python
function Install-Python {
    Write-Host "Checking for Python installation..."
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        Write-Host "Python3 not found. Installing Python..."
        winget install -e --id Python.Python.3 --silent
    } else {
        Write-Host "Python3 is already installed."
    }
}

# Function to install Git
function Install-Git {
    Write-Host "Checking for Git installation..."
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Git not found. Installing Git..."
        winget install -e --id Git.Git --silent
    } else {
        Write-Host "Git is already installed."
    }
}

# Function to install curl
function Install-Curl {
    Write-Host "Checking for curl installation..."
    if (-not (Get-Command curl -ErrorAction SilentlyContinue)) {
        Write-Host "curl not found. Installing curl..."
        winget install -e --id Curl.Curl --silent
    } else {
        Write-Host "curl is already installed."
    }
}

# Install dependencies
Install-Python
Install-Git
Install-Curl

# Clone the repository
Write-Host "Cloning the game repository..."
if (Test-Path "game") {
    Remove-Item -Recurse -Force "game"
}
git clone https://github.com/ShortTimeNoSee/echoes-of-time.git game
Set-Location "game"

# Set up virtual environment
Write-Host "Setting up virtual environment..."
python3 -m venv venv
.\venv\Scripts\Activate.ps1

# Install Pygame
Write-Host "Installing Pygame..."
pip install pygame --quiet

# Run the game
Write-Host "Running the game..."
python3 game.py
