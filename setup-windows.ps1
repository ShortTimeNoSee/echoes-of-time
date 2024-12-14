# Check if Python is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Python 3 not found. Installing Python..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install -e --id Python.Python.3
    } else {
        Write-Host "winget not found. Please install Python manually from https://www.python.org/"
        exit 1
    }
}

# Clone repository
Write-Host "Cloning the game repository..."
if (Test-Path "game") {
    Remove-Item -Recurse -Force "game"
}
git clone https://github.com/ShortTimeNoSee/echoes-of-time.git game
Set-Location "game"

# Set up virtual environment
Write-Host "Setting up a virtual environment..."
python3 -m venv venv
& .\venv\Scripts\Activate.ps1

# Install Pygame
Write-Host "Installing Pygame..."
pip install pygame

# Run the game
Write-Host "Running the game..."
python3 game.py
