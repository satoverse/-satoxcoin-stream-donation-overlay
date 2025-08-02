#!/usr/bin/env python3
"""
Quick Setup Script for Satoxcoin Stream Donation Overlay
Automates the initial configuration process
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("   Please edit .env with your actual credentials")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ env.example not found")
        return False

def create_satox_conf_example():
    """Create satoxcoin.conf.example if it doesn't exist"""
    satox_conf_example = Path("satoxcoin.conf.example")
    
    if not satox_conf_example.exists():
        print("❌ satoxcoin.conf.example not found")
        return False
    
    print("✅ satoxcoin.conf.example found")
    print("   Copy this file to your Satox data directory and rename to satoxcoin.conf")
    return True

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_validation():
    """Run configuration validation"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, "validate_config.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Configuration validation passed")
            return True
        else:
            print("❌ Configuration validation failed")
            print("   Please check the output above and fix any issues")
            return False
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Satoxcoin Stream Donation Overlay - Quick Setup")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    print("\n🐍 Checking Python version...")
    if not check_python_version():
        success = False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        success = False
    
    # Create .env file
    print("\n📝 Setting up configuration...")
    if not create_env_file():
        success = False
    
    # Check satoxcoin.conf example
    print("\n⚙️  Checking configuration examples...")
    if not create_satox_conf_example():
        success = False
    
    # Run validation
    print("\n🔍 Running configuration validation...")
    if not run_validation():
        success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 Quick setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Edit .env file with your credentials")
        print("   2. Create satoxcoin.conf in your Satox data directory")
        print("   3. Start Satox Core and wait for sync")
        print("   4. Run: python wallet_monitor.py")
        print("   5. Test: python -m http.server 8080")
        print("   6. Visit: http://localhost:8080/demo.html")
    else:
        print("❌ Quick setup encountered issues")
        print("\n💡 Please fix the issues above and try again")
        print("   For help, see README.md or README-WINDOWS.md")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 