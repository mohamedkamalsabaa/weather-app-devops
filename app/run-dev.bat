@echo off
REM Development script for Windows
REM Usage: run-dev.bat

echo Starting Weather App in Development Mode...
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run setup.bat first or copy .env.example to .env
    echo.
    pause
    exit /b 1
)

REM Load environment from .env file (python-dotenv will handle this)
echo Loading environment from .env file...

REM Check Python installation
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing/updating dependencies...
py -m pip install -r requirements.txt >nul

echo.
echo Starting Flask application...
echo Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop
echo.

REM Run the application
py app.py
