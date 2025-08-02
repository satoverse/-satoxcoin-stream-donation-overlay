#!/usr/bin/env python3
"""
Satoxcoin Twitch Donations - Simple Test Suite
Basic validation of code and dependencies.
"""

import os
import sys
import importlib
from pathlib import Path

def test_python_installation():
    """Test Python installation and version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} installed")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} too old, need 3.7+")
        return False

def test_core_modules():
    """Test core Python modules"""
    required_modules = ['json', 'time', 'logging', 'os', 'sys', 'datetime', 'typing']
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)
    
    if not missing_modules:
        print(f"✅ All {len(required_modules)} core modules available")
        return True
    else:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        return False

def test_requests_module():
    """Test requests module availability"""
    try:
        import requests
        print(f"✅ requests {requests.__version__} available")
        return True
    except ImportError:
        print("❌ requests module not found")
        return False

def test_required_files():
    """Test all required files exist"""
    required_files = [
        'wallet_monitor.py',
        'alert.html',
        'demo.html',
        'satox-logo.png',
        'coin.mp3'
    ]
    
    current_dir = Path(__file__).parent
    missing_files = []
    
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if not missing_files:
        print(f"✅ All {len(required_files)} required files present")
        return True
    else:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

def test_python_syntax():
    """Test Python syntax validation"""
    try:
        with open('wallet_monitor.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'wallet_monitor.py', 'exec')
        print("✅ wallet_monitor.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in wallet_monitor.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading wallet_monitor.py: {e}")
        return False

def test_wallet_monitor_import():
    """Test wallet monitor module import"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import wallet_monitor
        
        if hasattr(wallet_monitor, 'SatoxWalletMonitor'):
            print("✅ Module imports successfully with SatoxWalletMonitor class")
            return True
        else:
            print("❌ Module imported but SatoxWalletMonitor class not found")
            return False
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Satoxcoin Twitch Donations - Python Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Python Installation", test_python_installation),
        ("Core Python Modules", test_core_modules),
        ("Requests Module", test_requests_module),
        ("Required Files", test_required_files),
        ("Python Syntax", test_python_syntax),
        ("Wallet Monitor Import", test_wallet_monitor_import),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"[TEST] {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
            failed += 1
        print()
    
    # Summary
    print("=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Total Tests: {passed + failed}")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your setup is ready to use.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Check the output above for specific issues.")
    
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 