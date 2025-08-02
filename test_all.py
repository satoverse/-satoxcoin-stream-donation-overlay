#!/usr/bin/env python3
"""
Simple test file for Satoxcoin Stream Donation Overlay
This file is used by integration tests to verify the project structure.
"""

import os
import sys

def test_project_structure():
    """Test that the project has the required structure"""
    required_files = [
        'alert.html',
        'demo.html',
        'wallet_monitor.py',
        'satox-logo.png',
        'coin.mp3'
    ]
    
    missing_files = []
    for file_name in required_files:
        if not os.path.exists(file_name):
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def test_wallet_monitor_import():
    """Test that wallet_monitor.py can be imported"""
    try:
        from wallet_monitor import SatoxWalletMonitor, DonationAlert
        print("✅ wallet_monitor.py imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import wallet_monitor: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running project structure tests...")
    
    tests = [
        test_project_structure,
        test_wallet_monitor_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 