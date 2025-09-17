@echo off
title Android Doctor - Nokia G11 Recovery
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    ANDROID DOCTOR v1.0                      ║
echo  ║                Nokia G11 Recovery System                     ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.7+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python detected. Starting Android Doctor...
echo.

REM Install requirements if needed
if not exist "venv\" (
    echo [INFO] Setting up virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

echo [INFO] Running Nokia G11 recovery diagnosis...
echo.
python android_doctor.py

echo.
echo [INFO] Recovery process completed.
echo Check the logs folder for detailed information.
pause