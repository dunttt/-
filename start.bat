@echo off
chcp 936 >nul
title ShuHaiShiBei - Novel Platform
cd /d "%~dp0"

echo ========================================
echo    ShuHaiShiBei - Novel Platform
echo ========================================
echo Current Directory: %CD%
echo ========================================
echo.

REM Check Python
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not installed or not in PATH
    echo.
    echo Please install Python 3.9 or higher
    echo Download: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo [OK] Python is ready
echo.

REM Check dependencies
echo Checking project dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Dependencies not installed, installing...
    echo.
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies are ready
)
echo.

REM Start Flask application
echo Starting Flask application...
echo.
echo NOTE: Make sure MongoDB is running!
echo.

cls
echo ========================================
echo    [SUCCESS] Starting System...
echo ========================================
echo.
echo Access URLs:
echo    Local: http://127.0.0.1:5001
echo.
echo Test Accounts:
echo    Admin   - admin / admin123
echo    Creator - zuojia / creator123
echo    Reader  - duzhe / reader123
echo.
echo Tips:
echo    - Keep this window open
echo    - Press Ctrl+C to stop
echo ========================================
echo.

REM Start Flask app
python app.py

REM If app exits
echo.
echo ========================================
echo [WARN] Application stopped
echo ========================================
echo.
echo If you see connection errors, make sure MongoDB is running!
echo.
pause
