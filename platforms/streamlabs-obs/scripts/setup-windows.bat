@echo off
echo ========================================
echo Satoxcoin Twitch Donations Setup
echo Windows Compatibility Script
echo ========================================
echo.

REM Run dependency checker
call check-deps.bat
if errorlevel 1 (
    echo.
    echo ❌ Dependency check failed
    echo Please fix the issues above and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit wallet_monitor.py with your settings
echo 2. Run start-monitor.bat to start monitoring
echo 3. Add alert.html as Browser Source in OBS
echo.
echo For help, see README-WINDOWS.md
echo.
pause 