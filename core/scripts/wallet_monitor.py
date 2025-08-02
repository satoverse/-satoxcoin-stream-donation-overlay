#!/usr/bin/env python3
"""
Satoxcoin Twitch Donations Wallet Monitor
Copyright (c) Satoxcoin Core Developer

Monitors a Satox Core wallet for incoming donations and generates alerts for OBS overlay.
Windows-compatible version.
"""

import json
import time
import requests
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Windows compatibility imports
try:
    import msvcrt  # Windows-specific
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

# Configuration
RPC_USER = "your_rpc_username"
RPC_AUTH_TOKEN = "your_rpc_password"
RPC_HOST = "127.0.0.1"
RPC_PORT = 7777  # Satoxcoin RPC port (from official spec)
DONATION_ADDRESS = "your_donation_address_here"
MIN_DONATION = 100.0  # Minimum donation amount in SATOX
DEBUG = False

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

class SatoxWalletMonitor:
    def __init__(self):
        self.rpc_url = f"http://{RPC_HOST}:{RPC_PORT}"
        self.rpc_auth = (RPC_USER, RPC_AUTH_TOKEN)
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
                return msvcrt.kbhit() and msvcrt.getch() in [b'q', b'Q', b'\x03']  # q, Q, or Ctrl+C
            except:
                pass
        return False
    
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
    """Main entry point"""
    print("=" * 50)
    print("Satoxcoin Twitch Donations Monitor")
    print("Windows-Compatible Version")
    print("Copyright (c) Satoxcoin Core Developer")
    print("=" * 50)
    
    # Check configuration
    if RPC_USER == "your_rpc_username" or RPC_AUTH_TOKEN == "your_rpc_password":
        print("❌ ERROR: Please configure RPC_USER and RPC_AUTH_TOKEN in the script")
        print("Edit the configuration section at the top of this file")
        input("Press Enter to exit...")
        return
    
    if DONATION_ADDRESS == "your_donation_address_here":
        print("❌ ERROR: Please set your donation address in DONATION_ADDRESS")
        print("Edit the configuration section at the top of this file")
        input("Press Enter to exit...")
        return
    
    # Start monitor
    monitor = SatoxWalletMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
