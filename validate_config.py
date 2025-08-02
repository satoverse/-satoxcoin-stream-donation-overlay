#!/usr/bin/env python3
"""
Configuration Validation Script for Satoxcoin Stream Donation Overlay
Validates all configuration settings before starting the monitor
"""

import os
import sys
import requests
import json
from typing import List, Dict, Any

def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("✅ Loaded configuration from .env file")
        except Exception as e:
            print(f"⚠️  Warning: Could not load .env file: {e}")

def get_config() -> Dict[str, Any]:
    """Get configuration from environment variables or defaults"""
    return {
        'rpc_user': os.getenv("SATOX_RPC_USER", "your_rpc_username"),
        'rpc_password': os.getenv("SATOX_RPC_PASSWORD", "your_rpc_password"),
        'rpc_host': os.getenv("SATOX_RPC_HOST", "127.0.0.1"),
        'rpc_port': int(os.getenv("SATOX_RPC_PORT", "7777")),
        'donation_address': os.getenv("SATOX_DONATION_ADDRESS", "your_donation_address_here"),
        'min_donation': float(os.getenv("SATOX_MIN_DONATION", "1.0")),
        'debug': os.getenv("SATOX_DEBUG", "false").lower() == "true"
    }

def validate_satox_address(address: str) -> bool:
    """Validate Satoxcoin address format"""
    if not address or len(address) < 26 or len(address) > 35:
        return False
    if not address.startswith('S'):
        return False
    # Basic format check
    return all(c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' for c in address)

def test_rpc_connection(config: Dict[str, Any]) -> bool:
    """Test connection to Satox Core RPC"""
    try:
        url = f"http://{config['rpc_host']}:{config['rpc_port']}"
        headers = {'Content-Type': 'application/json'}
        data = {
            'jsonrpc': '1.0',
            'id': 'test',
            'method': 'getinfo',
            'params': []
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=data,
            auth=(config['rpc_user'], config['rpc_password']),
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result and 'error' not in result:
                print(f"✅ RPC connection successful")
                print(f"   Satox Core version: {result['result'].get('version', 'Unknown')}")
                return True
            else:
                print(f"❌ RPC error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ RPC connection failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Satox Core RPC")
        print("   Please ensure Satox Core is running and RPC is enabled")
        return False
    except requests.exceptions.Timeout:
        print("❌ RPC connection timed out")
        return False
    except Exception as e:
        print(f"❌ RPC connection error: {e}")
        return False

def check_required_files() -> bool:
    """Check that all required files exist"""
    required_files = [
        'wallet_monitor.py',
        'alert.html',
        'demo.html',
        'satox-logo.png',
        'coin.mp3',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_python_dependencies() -> bool:
    """Check that Python dependencies are installed"""
    try:
        import requests
        print("✅ Python dependencies installed")
        return True
    except ImportError:
        print("❌ Missing Python dependencies")
        print("   Run: pip install -r requirements.txt")
        return False

def validate_configuration(config: Dict[str, Any]) -> List[str]:
    """Validate configuration settings"""
    errors = []
    
    # Check for placeholder values
    if config['rpc_user'] in ["your_rpc_username", "your_username", "your_actual_username"]:
        errors.append("RPC_USER not configured")
    
    if config['rpc_password'] in ["your_rpc_password", "your_password", "your_actual_password"]:
        errors.append("RPC_PASSWORD not configured")
    
    if config['donation_address'] in ["your_donation_address_here", "your_address", "your_actual_address", "YOUR_DONATION_ADDRESS_HERE", "SQBurnSatoXAddressXXXXXXXXXXUqEipi"]:
        errors.append("DONATION_ADDRESS not configured")
    
    # Validate donation address format
    if not validate_satox_address(config['donation_address']):
        errors.append("Invalid donation address format")
    
    # Validate port number
    if not (1024 <= config['rpc_port'] <= 65535):
        errors.append("Invalid RPC port number")
    
    # Validate minimum donation
    if config['min_donation'] <= 0:
        errors.append("Minimum donation must be greater than 0")
    
    return errors

def main():
    """Main validation function"""
    print("🔍 Satoxcoin Stream Donation Overlay - Configuration Validator")
    print("=" * 60)
    
    # Load environment variables
    load_env_file()
    
    # Get configuration
    config = get_config()
    
    # Display current configuration
    print("\n📋 Current Configuration:")
    print(f"   RPC Host: {config['rpc_host']}:{config['rpc_port']}")
    print(f"   RPC User: {config['rpc_user']}")
    print(f"   Donation Address: {config['donation_address'][:8]}...{config['donation_address'][-4:]}")
    print(f"   Minimum Donation: {config['min_donation']} SATOX")
    print(f"   Debug Mode: {config['debug']}")
    
    # Validate configuration
    print("\n🔍 Validating Configuration...")
    config_errors = validate_configuration(config)
    
    if config_errors:
        print("❌ Configuration Errors:")
        for error in config_errors:
            print(f"   - {error}")
        print("\n📝 To fix these issues:")
        print("   1. Set environment variables:")
        print("      export SATOX_RPC_USER='your_username'")
        print("      export SATOX_RPC_PASSWORD='your_password'")
        print("      export SATOX_DONATION_ADDRESS='your_address'")
        print("   2. Or edit wallet_monitor.py directly")
        print("   3. Or create a .env file with your settings")
        return 1
    
    print("✅ Configuration validation passed")
    
    # Check required files
    print("\n📁 Checking Required Files...")
    if not check_required_files():
        return 1
    
    # Check Python dependencies
    print("\n🐍 Checking Python Dependencies...")
    if not check_python_dependencies():
        return 1
    
    # Test RPC connection
    print("\n🔗 Testing RPC Connection...")
    if not test_rpc_connection(config):
        print("\n💡 Troubleshooting RPC Connection:")
        print("   1. Ensure Satox Core is running")
        print("   2. Check satoxcoin.conf settings")
        print("   3. Verify RPC credentials")
        print("   4. Check firewall settings")
        return 1
    
    # All tests passed
    print("\n" + "=" * 60)
    print("🎉 All validations passed! Your setup is ready.")
    print("\n🚀 Next steps:")
    print("   1. Start the monitor: python wallet_monitor.py")
    print("   2. Test the demo: python -m http.server 8080")
    print("   3. Visit: http://localhost:8080/demo.html")
    print("   4. Add alert.html as Browser Source in OBS")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 