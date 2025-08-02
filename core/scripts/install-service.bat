@echo off
echo ========================================
echo Satoxcoin Donation Monitor Service
echo Windows Service Installer
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

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

echo Installing Satoxcoin Donation Monitor as Windows Service...
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Create service using NSSM (if available) or sc command
echo Creating service...

REM Try using sc command (built into Windows)
sc create "SatoxcoinDonationMonitor" binPath= "python \"%SCRIPT_DIR%\wallet_monitor.py\"" start= auto DisplayName= "Satoxcoin Donation Monitor"

if %errorLevel% == 0 (
    echo ✅ Service created successfully
    echo.
    echo Service Details:
    echo - Name: SatoxcoinDonationMonitor
    echo - Display Name: Satoxcoin Donation Monitor
    echo - Startup: Automatic
    echo - Path: %SCRIPT_DIR%\wallet_monitor.py
    echo.
    echo To start the service:
    echo   net start SatoxcoinDonationMonitor
    echo.
    echo To stop the service:
    echo   net stop SatoxcoinDonationMonitor
    echo.
    echo To remove the service:
    echo   sc delete SatoxcoinDonationMonitor
    echo.
    echo ⚠️  IMPORTANT: Make sure to configure wallet_monitor.py before starting!
) else (
    echo ❌ Failed to create service
    echo.
    echo Alternative: Use NSSM (Non-Sucking Service Manager)
    echo 1. Download NSSM from https://nssm.cc/
    echo 2. Run: nssm install SatoxcoinDonationMonitor
    echo 3. Set Application: python
    echo 4. Set App Parameters: "%SCRIPT_DIR%\wallet_monitor.py"
)

echo.
pause 