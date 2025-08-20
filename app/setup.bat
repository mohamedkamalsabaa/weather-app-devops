@echo off
REM Setup script for Weather App
echo Weather App Setup
echo =================
echo.

REM Check Python
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found: 
py --version
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file and add your OpenWeatherMap API key!
    echo Get your free API key from: https://openweathermap.org/api
    echo.
) else (
    echo .env file already exists
)

REM Install dependencies
echo Installing Python dependencies...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenWeatherMap API key
echo 2. Run: run-dev.bat
echo.
pause
