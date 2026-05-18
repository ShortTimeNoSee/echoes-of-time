# Echoes of Time
* Use echoes to destroy enemies.
* Increasing difficulty with each level.
* Probably a bug or two or twenty.

## Easy Installation

Choose the command below that matches your operating system. Open your terminal and paste it in.

### Mac, Linux, or WSL (Ubuntu, Debian, etc.)
```bash
curl -fsSL https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-launcher.sh | bash
```

### Windows (PowerShell)
Open **PowerShell** (not CMD) and run:
```powershell
powershell -ExecutionPolicy Bypass -Command "Invoke-Expression (Invoke-RestMethod 'https://raw.githubusercontent.com/ShortTimeNoSee/echoes-of-time/main/setup-windows.ps1')"
```

### ⚠️⚠️⚠️
When running the setup script, the game will be cloned into a folder named `game`. If a folder named `game` already exists in the current directory, it will be deleted and replaced. Make sure you don't have important files in a folder named `game` before running the setup.
### ⚠️⚠️⚠️

## Controls
* Move: Arrow keys
* Create Echo: Press `E`
* Pause Game: Press `P`

## Requirements
* Python 3.x
* Pygame library

If missing, the setup script will handle everything.

## File structure
```
echoes-of-time/
├── bootstrap.sh        # POSIX-compatible setup script (Linux/macOS)
├── setup-windows.ps1   # Windows PowerShell setup script
├── setup-launcher.sh   # Unified launcher for detecting OS and running the appropriate script
├── play.sh             # Cross-platform game launcher (POSIX-based environments)
├── play.ps1            # Game launcher for Windows (PowerShell)
├── game.py             # Game logic
├── README.md           # Game instructions and details
├── LICENSE             # Licensing information
└── sounds/             # Sound effects
    ├── echo.wav
    ├── death.wav
    ├── shatter.wav
    ├── level_up.wav
    └── pause.wav
```

## License
MIT License. Use, modify, and distribute freely.
