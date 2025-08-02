@echo off
title Satoxcoin Donations Demo
echo ========================================
echo Satoxcoin Twitch Donations Demo
echo Starting local server...
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

echo ✅ Starting demo server on http://localhost:8080
echo ✅ Open http://localhost:8080/demo.html in your browser
echo ✅ Press Ctrl+C to stop the server
echo.

REM Start Python HTTP server
python -m http.server 8080

echo.
echo Demo server stopped.
pause 