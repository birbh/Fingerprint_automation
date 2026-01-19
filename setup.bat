@echo off
REM Quick Start Script for Windows

echo ==================================
echo Fingerprint Automation System
echo Quick Start Script
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo         Install Python 3 first: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found

REM Install requirements
echo.
echo Installing Python requirements...
cd python_backend
pip install -r requirements.txt

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Upload arduino_fingerprint.ino to your Arduino
echo 2. Connect fingerprint sensor to Arduino
echo 3. Run: python fingerprint_app.py -p COM3
echo    (Replace COM3 with your Arduino port)
echo.
echo For detailed instructions, see docs\GUIDE.md
echo.
pause
