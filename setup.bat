@echo off
chcp 936 >nul
title ShuHaiShiBei - Setup
cd /d "%~dp0"

echo ========================================
echo       ShuHaiShiBei - One-Click Setup
echo ========================================
echo Current Directory: %CD%
echo ========================================
echo.
echo This script will:
echo 1. Check Python
echo 2. Install dependencies
echo 3. Initialize database
echo 4. Create test accounts
echo.
echo Press any key to start...
pause >nul
cls

REM Check Python
echo ========================================
echo [1/3] Checking Python...
echo ========================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    echo.
    echo Please install Python 3.9 or higher
    echo Download: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python is ready
echo.
pause

REM Install dependencies
cls
echo ========================================
echo [2/3] Installing Dependencies...
echo ========================================
echo.
echo Using Tsinghua mirror to install packages...
echo (This may take 1-3 minutes, please wait)
echo.

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Possible reasons:
    echo 1. Network connection issue
    echo 2. pip version too old
    echo.
    echo Try upgrading pip first:
    echo python -m pip install --upgrade pip
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully
echo.
pause

REM Initialize database
cls
echo ========================================
echo [3/3] Initializing Database...
echo ========================================
echo.
echo NOTE: Make sure MongoDB is running!
echo.
echo If MongoDB is not running:
echo   - Open Services (services.msc)
echo   - Find "MongoDB Server"
echo   - Right-click and select "Start"
echo.
echo Creating database and test accounts...
echo.

python init_data.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Database initialization failed
    echo.
    echo Make sure MongoDB is running!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Setup Complete!
echo ========================================
echo.
echo Test accounts created:
echo   Admin   - admin / admin123
echo   Creator - zuojia / creator123
echo   Reader  - duzhe / reader123
echo.
echo Next steps:
echo   Double-click "start.bat" to start the system
echo   Then visit http://127.0.0.1:5001
echo.
echo ========================================
echo.
pause
