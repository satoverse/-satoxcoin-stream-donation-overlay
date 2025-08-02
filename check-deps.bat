@echo off
REM ========================================
REM Satoxcoin Dependencies Checker
REM Checks and installs missing dependencies
REM ========================================

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
echo.
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip not found
    echo Please reinstall Python with pip included
    exit /b 1
)

echo ✅ pip found
pip --version

REM Check core Python modules
echo.
echo Checking core Python modules...
python -c "import json, time, logging, os, sys, datetime, typing" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Missing core Python modules
    echo This indicates a Python installation issue
    exit /b 1
)

echo ✅ Core Python modules available

REM Check for requests module
echo.
echo Checking requests module...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Missing dependency: requests
    echo Installing requests...
    pip install requests
    if errorlevel 1 (
        echo ❌ ERROR: Failed to install requests
        echo Please check your internet connection and try again
        exit /b 1
    )
    echo ✅ requests installed successfully
) else (
    echo ✅ requests already installed
)

REM Check for http.server (for demo)
echo.
echo Checking HTTP server modules...
python -c "import http.server, socketserver" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Missing HTTP server modules
    echo This indicates a Python installation issue
    exit /b 1
)

echo ✅ HTTP server modules available

REM Final verification
echo.
echo Final verification...
python -c "import requests; print('✅ All dependencies verified successfully')" 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Final verification failed
    exit /b 1
)

echo.
echo ========================================
echo ✅ All dependencies are ready!
echo ========================================
exit /b 0 