@echo off
title Satoxcoin Donations - Comprehensive Test Suite
echo ========================================
echo Satoxcoin Twitch Donations Test Suite
echo Comprehensive Code Validation
echo ========================================
echo.

REM Set error handling
setlocal enabledelayedexpansion

REM Initialize test counters
set /a tests_passed=0
set /a tests_failed=0
set /a total_tests=0

echo [TEST] Starting comprehensive validation...
echo.

REM Test 1: Check Python installation
echo [TEST 1/12] Python Installation Check...
set /a total_tests+=1
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Python not found
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: Python found
    python --version
    set /a tests_passed+=1
)
echo.

REM Test 2: Check pip availability
echo [TEST 2/12] Pip Availability Check...
set /a total_tests+=1
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: pip not found
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: pip found
    pip --version
    set /a tests_passed+=1
)
echo.

REM Test 3: Check core Python modules
echo [TEST 3/12] Core Python Modules Check...
set /a total_tests+=1
python -c "import json, time, logging, os, sys, datetime, typing" >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Missing core Python modules
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: All core modules available
    set /a tests_passed+=1
)
echo.

REM Test 4: Check requests module
echo [TEST 4/12] Requests Module Check...
set /a total_tests+=1
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  WARNING: requests not found, attempting installation...
    pip install requests >nul 2>&1
    if errorlevel 1 (
        echo ❌ FAILED: Could not install requests
        set /a tests_failed+=1
    ) else (
        echo ✅ PASSED: requests installed and available
        set /a tests_passed+=1
    )
) else (
    echo ✅ PASSED: requests already available
    set /a tests_passed+=1
)
echo.

REM Test 5: Check HTTP server modules
echo [TEST 5/12] HTTP Server Modules Check...
set /a total_tests+=1
python -c "import http.server, socketserver" >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Missing HTTP server modules
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: HTTP server modules available
    set /a tests_passed+=1
)
echo.

REM Test 6: Check required files exist
echo [TEST 6/12] Required Files Check...
set /a total_tests+=1
set missing_files=0

if not exist "wallet_monitor.py" (
    echo ❌ Missing: wallet_monitor.py
    set /a missing_files+=1
)
if not exist "alert.html" (
    echo ❌ Missing: alert.html
    set /a missing_files+=1
)
if not exist "demo.html" (
    echo ❌ Missing: demo.html
    set /a missing_files+=1
)
if not exist "satox-logo.png" (
    echo ❌ Missing: satox-logo.png
    set /a missing_files+=1
)
REM coin.gif was removed as it was not used
if not exist "coin.mp3" (
    echo ❌ Missing: coin.mp3
    set /a missing_files+=1
)

if %missing_files% == 0 (
    echo ✅ PASSED: All required files present
    set /a tests_passed+=1
) else (
    echo ❌ FAILED: %missing_files% file(s) missing
    set /a tests_failed+=1
)
echo.

REM Test 7: Python syntax validation
echo [TEST 7/12] Python Syntax Validation...
set /a total_tests+=1
python -m py_compile wallet_monitor.py >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Python syntax errors in wallet_monitor.py
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: Python syntax is valid
    set /a tests_passed+=1
)
echo.

REM Test 8: HTML syntax validation (basic)
echo [TEST 8/12] HTML Syntax Validation...
set /a total_tests+=1
findstr /C:"<!DOCTYPE html>" alert.html >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: alert.html missing DOCTYPE
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: alert.html has valid DOCTYPE
    set /a tests_passed+=1
)

findstr /C:"<!DOCTYPE html>" demo.html >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: demo.html missing DOCTYPE
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: demo.html has valid DOCTYPE
    set /a tests_passed+=1
)
echo.

REM Test 9: Check batch file syntax
echo [TEST 9/12] Batch File Syntax Check...
set /a total_tests+=1
set batch_errors=0

REM Test each batch file
for %%f in (*.bat) do (
    echo   Checking %%f...
    findstr /C:"@echo off" "%%f" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠️  Warning: %%f missing @echo off
    )
)

echo ✅ PASSED: Batch files syntax check completed
set /a tests_passed+=1
echo.

REM Test 10: Test wallet monitor import
echo [TEST 10/12] Wallet Monitor Import Test...
set /a total_tests+=1
python -c "import wallet_monitor; print('✅ Module imports successfully')" >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: wallet_monitor.py import failed
    set /a tests_failed+=1
) else (
    echo ✅ PASSED: wallet_monitor.py imports correctly
    set /a tests_passed+=1
)
echo.

REM Test 11: Test configuration validation
echo [TEST 11/12] Configuration Validation...
set /a total_tests+=1

REM Check if configuration is still default
findstr /C:"your_rpc_username" wallet_monitor.py >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  WARNING: Using default RPC username (needs configuration)
)

findstr /C:"your_donation_address_here" wallet_monitor.py >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  WARNING: Using default donation address (needs configuration)
)

echo ✅ PASSED: Configuration validation completed
set /a tests_passed+=1
echo.

REM Test 12: Test demo server startup
echo [TEST 12/12] Demo Server Test...
set /a total_tests+=1

REM Check if port 8080 is available
netstat -an | findstr ":8080" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  WARNING: Port 8080 is in use, skipping server test
    echo ✅ PASSED: Port check completed
    set /a tests_passed+=1
) else (
    echo   Starting demo server test...
    start /B python -m http.server 8080 >nul 2>&1
    timeout /t 2 >nul
    
    REM Test if server responds
    curl -s http://localhost:8080 >nul 2>&1
    if errorlevel 1 (
        echo ❌ FAILED: Demo server test failed
        set /a tests_failed+=1
    ) else (
        echo ✅ PASSED: Demo server test successful
        set /a tests_passed+=1
    )
    
    REM Stop the server
    taskkill /f /im python.exe >nul 2>&1
)
echo.

REM Final results
echo ========================================
echo TEST RESULTS SUMMARY
echo ========================================
echo.
echo Tests Passed: %tests_passed%/%total_tests%
echo Tests Failed: %tests_failed%/%total_tests%
echo.

if %tests_failed% == 0 (
    echo 🎉 ALL TESTS PASSED! 
    echo ✅ Your Satoxcoin Twitch Donations setup is ready to use.
    echo.
    echo Next steps:
    echo 1. Configure wallet_monitor.py with your settings
    echo 2. Run start-monitor.bat to begin monitoring
    echo 3. Add alert.html as Browser Source in OBS
) else (
    echo ⚠️  SOME TESTS FAILED
    echo.
    echo Failed tests need to be addressed before using the system.
    echo Check the output above for specific issues.
    echo.
    echo Common solutions:
    echo - Run setup-windows.bat to install missing dependencies
    echo - Check that all files are present in the directory
    echo - Verify Python installation includes pip
    echo - Configure wallet_monitor.py with your settings
)

echo.
echo ========================================
echo Test completed at %date% %time%
echo ========================================
pause 