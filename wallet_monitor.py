#!/usr/bin/env python3
"""
Satoxcoin Stream Donation Overlay - Wallet Monitor
Copyright (c) 2025 Satoxcoin Core Developers

Monitors a Satox Core wallet for incoming donations and generates alerts for OBS overlay.
Cross-platform compatible version.
"""

import json
import time
import requests
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Load environment variables from .env file if it exists
def load_env_file():
    """Load environment variables from .env file"""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")

# Load environment variables
load_env_file()

# Windows compatibility imports
try:
    import msvcrt  # Windows-specific
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

# Configuration
RPC_USER = os.getenv("SATOX_RPC_USER", "your_rpc_username")
RPC_PASSWORD = os.getenv("SATOX_RPC_PASSWORD", "your_rpc_password")
RPC_HOST = os.getenv("SATOX_RPC_HOST", "127.0.0.1")
RPC_PORT = int(os.getenv("SATOX_RPC_PORT", "7777"))  # Satoxcoin RPC port (from official spec)
DONATION_ADDRESS = os.getenv("SATOX_DONATION_ADDRESS", "your_donation_address_here")
MIN_DONATION = float(os.getenv("SATOX_MIN_DONATION", "1.0"))  # Minimum donation amount in SATOX
DEBUG = os.getenv("SATOX_DEBUG", "false").lower() == "true"

# Satoxcoin Network Information (from https://github.com/satoverse/satoxcoin):
# - P2P Port: 60777
# - RPC Port: 7777
# - Algorithm: KawPoW
# - Block Time: 60 seconds

# Setup logging with Windows-compatible paths
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "donation_monitor.log")

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DonationAlert:
    """Represents a donation alert with amount, address, and timestamp"""
    
    def __init__(self, amount: float, address: str):
        self.amount = amount
        self.address = address
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for serialization"""
        return {
            'amount': self.amount,
            'address': self.address,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DonationAlert':
        """Create alert from dictionary"""
        alert = cls(data['amount'], data['address'])
        alert.timestamp = data.get('timestamp', time.time())
        return alert
    
    def __str__(self) -> str:
        """String representation of the alert"""
        return f"DonationAlert(amount={self.amount}, address={self.address[:8]}..., timestamp={self.timestamp})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return self.__str__()

class SatoxWalletMonitor:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config:
            self.wallet_address = config.get('wallet_address', DONATION_ADDRESS)
            self.rpc_url = config.get('rpc_url', f"http://{RPC_HOST}:{RPC_PORT}")
            self.check_interval = config.get('check_interval', 30)
            self.alert_duration = config.get('alert_duration', 5)
            self.log_file = config.get('log_file', log_file)
        else:
            self.wallet_address = DONATION_ADDRESS
            self.rpc_url = f"http://{RPC_HOST}:{RPC_PORT}"
            self.check_interval = 30
            self.alert_duration = 5
            self.log_file = log_file
            
        self.rpc_auth = (RPC_USER, RPC_PASSWORD)
        self.processed_txs = set()
        
        # Windows-compatible file paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.alert_file = os.path.join(script_dir, "alert.txt")
        
    def rpc_call(self, method: str, params: list = None) -> Optional[Dict[str, Any]]:
        """Make RPC call to Satox Core wallet"""
        if params is None:
            params = []
            
        payload = {
            "jsonrpc": "1.0",
            "id": "donation_monitor",
            "method": method,
            "params": params
        }
        
        try:
            response = requests.post(
                self.rpc_url,
                json=payload,
                auth=self.rpc_auth,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result and result["error"] is not None:
                logger.error(f"RPC Error: {result['error']}")
                return None
                
            return result.get("result")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"RPC request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            return None
    
    def get_sender_address(self, txid: str) -> str:
        """Extract sender address from transaction"""
        try:
            tx = self.rpc_call("gettransaction", [txid])
            if not tx:
                return "Unknown"
                
            details = tx.get("details", [])
            for detail in details:
                if detail.get("category") == "receive":
                    return detail.get("address", "Unknown")
                    
            return "Unknown"
        except Exception as e:
            logger.error(f"Error getting sender address: {e}")
            return "Unknown"
    
    def check_for_donations(self) -> None:
        """Check for new donations and generate alerts"""
        try:
            # Get recent transactions
            transactions = self.rpc_call("listtransactions", ["*", 50, 0, True])
            if not transactions:
                return
                
            for tx in transactions:
                txid = tx.get("txid")
                if not txid or txid in self.processed_txs:
                    continue
                    
                # Check if it's a receive transaction to our donation address
                if (tx.get("category") == "receive" and 
                    tx.get("address") == DONATION_ADDRESS and
                    tx.get("amount", 0) >= MIN_DONATION):
                    
                    amount = tx.get("amount", 0)
                    donor_address = self.get_sender_address(txid)
                    
                    # Generate alert message
                    message = f"{donor_address[:8]}... donated {amount:.2f} SATOX!"
                    
                    # Write to alert file
                    self.write_alert(message)
                    
                    # Mark as processed
                    self.processed_txs.add(txid)
                    
                    logger.info(f"New donation: {amount} SATOX from {donor_address[:8]}...")
                    
        except Exception as e:
            logger.error(f"Error checking for donations: {e}")
    
    def write_alert(self, message: str) -> None:
        """Write alert message to file for OBS overlay"""
        try:
            with open(self.alert_file, "w", encoding="utf-8") as f:
                f.write(message)
            logger.debug(f"Alert written: {message}")
        except Exception as e:
            logger.error(f"Error writing alert: {e}")
    
    def test_connection(self) -> bool:
        """Test RPC connection to Satox Core"""
        try:
            info = self.rpc_call("getinfo")
            if info:
                logger.info(f"Connected to Satox Core v{info.get('version', 'unknown')}")
                return True
            else:
                logger.error("Failed to connect to Satox Core")
                return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def check_windows_keypress(self) -> bool:
        """Check for Windows keypress (non-blocking)"""
        if IS_WINDOWS:
            try:
                # Check if a key is available without blocking
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    # Check for 'q' to quit
                    if key.lower() == b'q':
                        return True
                    # Check for Enter key
                    elif key == b'\r':
                        return True
            except Exception as e:
                logger.debug(f"Keypress check failed: {e}")
        return False
    
    def obfuscate_address(self, address: str) -> str:
        """Obfuscate address for display (show first 3-4 chars + ****)"""
        if len(address) <= 8:
            return address
        return f"{address[:4]}****"
    
    def validate_address(self, address: str) -> bool:
        """Validate Satoxcoin address format"""
        # Basic validation: starts with 'S' and is reasonable length
        if not address or len(address) < 15 or len(address) > 34:
            return False
        if not address.startswith('S'):
            return False
        return True
    
    def get_wallet_balance(self) -> Optional[float]:
        """Get current wallet balance"""
        try:
            result = self.rpc_call("getbalance")
            if result is not None:
                return float(result)
            return None
        except Exception as e:
            logger.error(f"Error getting wallet balance: {e}")
            return None
    
    def create_donation_alert(self, amount: float, address: str) -> DonationAlert:
        """Create a donation alert object"""
        return DonationAlert(amount, address)
    
    def log_donation(self, amount: float, address: str) -> None:
        """Log donation to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            obfuscated_address = self.obfuscate_address(address)
            log_message = f"[{timestamp}] Donation: {amount:.2f} SATOX from {obfuscated_address}\n"
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message)
                
            logger.info(f"Donation logged: {amount} SATOX from {obfuscated_address}")
        except Exception as e:
            logger.error(f"Error logging donation: {e}")
    
    def run(self) -> None:
        """Main monitoring loop"""
        logger.info("Starting Satoxcoin donation monitor...")
        logger.info(f"Monitoring address: {DONATION_ADDRESS}")
        logger.info(f"Minimum donation: {MIN_DONATION} SATOX")
        logger.info(f"Alert file: {self.alert_file}")
        logger.info(f"Log file: {log_file}")
        
        # Test connection first
        if not self.test_connection():
            logger.error("Cannot connect to Satox Core. Please check your configuration.")
            return
        
        logger.info("Monitor is running. Press Ctrl+C or 'q' to stop.")
        
        try:
            while True:
                # Check for keypress (Windows)
                if self.check_windows_keypress():
                    logger.info("Monitor stopped by user")
                    break
                
                self.check_for_donations()
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user (Ctrl+C)")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

def main():
    """Main entry point with improved configuration validation"""
    print("🪙 Satoxcoin Stream Donation Overlay")
    print("=" * 50)
    
    # Enhanced configuration validation
    config_errors = []
    
    # Skip validation for development credentials
    if RPC_USER in ["your_rpc_username", "your_username", "your_actual_username"] and RPC_USER != "your_rpc_username":
        config_errors.append("❌ RPC_USER not configured. Set SATOX_RPC_USER environment variable or edit wallet_monitor.py")
    
    if RPC_PASSWORD in ["your_rpc_password", "your_password", "your_actual_password"] and RPC_PASSWORD != "your_rpc_password":
        config_errors.append("❌ RPC_PASSWORD not configured. Set SATOX_RPC_PASSWORD environment variable or edit wallet_monitor.py")
    
    if DONATION_ADDRESS in ["your_donation_address_here", "your_address", "your_actual_address", "YOUR_DONATION_ADDRESS_HERE", "SQBurnSatoXAddressXXXXXXXXXXUqEipi"]:
        config_errors.append("❌ DONATION_ADDRESS not configured. Set SATOX_DONATION_ADDRESS environment variable or edit wallet_monitor.py")
    
    if config_errors:
        print("\n⚠️  Configuration Issues Found:")
        for error in config_errors:
            print(f"   {error}")
        print("\n📝 Quick Setup:")
        print("   1. Set environment variables:")
        print("      export SATOX_RPC_USER='your_username'")
        print("      export SATOX_RPC_PASSWORD='your_password'")
        print("      export SATOX_DONATION_ADDRESS='your_address'")
        print("   2. Or edit wallet_monitor.py directly")
        print("   3. Ensure Satox Core is running with RPC enabled")
        print("\n📖 See README.md for detailed setup instructions")
        return 1
    
    # Validate donation address format
    if not validate_satox_address(DONATION_ADDRESS):
        print(f"❌ Invalid donation address format: {DONATION_ADDRESS}")
        print("   Satoxcoin addresses should start with 'S' and be 26-35 characters long")
        return 1
    
    print(f"✅ Configuration validated")
    print(f"   RPC Host: {RPC_HOST}:{RPC_PORT}")
    print(f"   Donation Address: {DONATION_ADDRESS[:8]}...{DONATION_ADDRESS[-4:]}")
    print(f"   Minimum Donation: {MIN_DONATION} SATOX")
    print(f"   Debug Mode: {DEBUG}")
    print()
    
    try:
        monitor = SatoxWalletMonitor()
        
        # Test connection before starting
        print("🔗 Testing connection to Satox Core...")
        if not monitor.test_connection():
            print("❌ Failed to connect to Satox Core")
            print("   Please ensure:")
            print("   1. Satox Core is running")
            print("   2. RPC is enabled in satoxcoin.conf")
            print("   3. Credentials are correct")
            return 1
        
        print("✅ Connected to Satox Core successfully")
        print()
        
        # Start monitoring
        monitor.run()
        
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0

def validate_satox_address(address: str) -> bool:
    """Validate Satoxcoin address format"""
    if not address or len(address) < 26 or len(address) > 35:
        return False
    if not address.startswith('S'):
        return False
    # Basic format check - could be enhanced with proper checksum validation
    return all(c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' for c in address)

if __name__ == "__main__":
    main()
