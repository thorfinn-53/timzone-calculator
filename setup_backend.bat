@echo off
echo ==============================
echo Setting up Python backend venv
echo ==============================

REM Check if Python is installed
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python was not found on this system.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, make sure to enable:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python found.

REM Create venv if it does not exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        echo Make sure Python is installed correctly and added to PATH.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate venv
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment.
    echo Try deleting the venv folder and running this setup again.
    echo.
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo ERROR: Failed to upgrade pip.
    echo.
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install requirements.
    echo Make sure requirements.txt exists and is valid.
    echo.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully.
pause