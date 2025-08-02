@echo off
title Satoxcoin Donation Monitor
echo ========================================
echo Satoxcoin Twitch Donations Monitor
echo Starting...
echo ========================================
echo.

REM Check dependencies
call check-deps.bat
if errorlevel 1 (
    echo.
    echo ❌ Dependency check failed
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

REM Check if wallet_monitor.py exists
if not exist "wallet_monitor.py" (
    echo ❌ ERROR: wallet_monitor.py not found
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

echo ✅ Starting donation monitor...
echo ✅ Press Ctrl+C to stop the monitor
echo.

REM Run the Python script
python wallet_monitor.py

echo.
echo Monitor stopped.
pause 