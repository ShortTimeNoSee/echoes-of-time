# Navigate to the game directory
Set-Location -Path "$PSScriptRoot\game"

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run the game
Write-Host "Running Echoes of Time..."
python3 game.py
