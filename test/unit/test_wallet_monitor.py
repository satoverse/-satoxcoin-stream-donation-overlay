#!/usr/bin/env python3
"""
Unit Tests for Satoxcoin Wallet Monitor
Tests individual components and functions
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path to import the wallet monitor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from wallet_monitor import SatoxWalletMonitor, DonationAlert
except ImportError:
    print("Warning: Could not import wallet_monitor. Make sure you're in the correct directory.")
    sys.exit(1)

class TestSatoxWalletMonitor(unittest.TestCase):
    """Unit tests for SatoxWalletMonitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            'wallet_address': 'S8f3test1234567890abcdef',
            'rpc_url': 'http://localhost:8332',
            'check_interval': 30,
            'alert_duration': 5,
            'log_file': 'test_donation_monitor.log'
        }
        self.monitor = SatoxWalletMonitor(self.test_config)
    
    def test_init(self):
        """Test monitor initialization"""
        self.assertEqual(self.monitor.wallet_address, self.test_config['wallet_address'])
        self.assertEqual(self.monitor.rpc_url, self.test_config['rpc_url'])
        self.assertEqual(self.monitor.check_interval, self.test_config['check_interval'])
        self.assertEqual(self.monitor.alert_duration, self.test_config['alert_duration'])
    
    def test_obfuscate_address(self):
        """Test address obfuscation"""
        test_address = "S8f3test1234567890abcdef"
        obfuscated = self.monitor.obfuscate_address(test_address)
        
        # Should show first 3-4 characters + ****
        self.assertTrue(obfuscated.startswith("S8f3"))
        self.assertTrue(obfuscated.endswith("****"))
        self.assertIn("****", obfuscated)
    
    def test_validate_address(self):
        """Test address validation"""
        # Valid Satoxcoin address
        valid_address = "S8f3test1234567890abcdef"
        self.assertTrue(self.monitor.validate_address(valid_address))
        
        # Invalid addresses
        invalid_addresses = [
            "invalid",
            "1234567890",
            "S8f3",  # Too short
            "S8f3test1234567890abcdefghijklmnopqrstuvwxyz"  # Too long
        ]
        
        for addr in invalid_addresses:
            self.assertFalse(self.monitor.validate_address(addr))
    
    @patch('requests.post')
    def test_get_wallet_balance(self, mock_post):
        """Test wallet balance retrieval"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': 150.75,
            'error': None
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        balance = self.monitor.get_wallet_balance()
        self.assertEqual(balance, 150.75)
    
    @patch('requests.post')
    def test_get_wallet_balance_error(self, mock_post):
        """Test wallet balance retrieval with error"""
        # Mock error response
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': None,
            'error': 'Connection failed'
        }
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        balance = self.monitor.get_wallet_balance()
        self.assertIsNone(balance)
    
    def test_create_donation_alert(self):
        """Test donation alert creation"""
        amount = 100.50
        address = "S8f3test1234567890abcdef"
        
        alert = self.monitor.create_donation_alert(amount, address)
        
        self.assertIsInstance(alert, DonationAlert)
        self.assertEqual(alert.amount, amount)
        self.assertEqual(alert.address, address)
        self.assertIsNotNone(alert.timestamp)
    
    def test_log_donation(self):
        """Test donation logging"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            self.monitor.log_file = temp_filename
            amount = 75.25
            address = "S8f3test1234567890abcdef"
            
            self.monitor.log_donation(amount, address)
            
            # Check if log file was created and contains the donation
            with open(temp_filename, 'r') as f:
                log_content = f.read()
                self.assertIn(str(amount), log_content)
                self.assertIn(self.monitor.obfuscate_address(address), log_content)
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TestDonationAlert(unittest.TestCase):
    """Unit tests for DonationAlert class"""
    
    def test_donation_alert_creation(self):
        """Test DonationAlert object creation"""
        amount = 50.00
        address = "S8f3test1234567890abcdef"
        
        alert = DonationAlert(amount, address)
        
        self.assertEqual(alert.amount, amount)
        self.assertEqual(alert.address, address)
        self.assertIsNotNone(alert.timestamp)
    
    def test_donation_alert_to_dict(self):
        """Test DonationAlert serialization"""
        amount = 25.75
        address = "S8f3test1234567890abcdef"
        
        alert = DonationAlert(amount, address)
        alert_dict = alert.to_dict()
        
        self.assertEqual(alert_dict['amount'], amount)
        self.assertEqual(alert_dict['address'], address)
        self.assertIn('timestamp', alert_dict)
    
    def test_donation_alert_from_dict(self):
        """Test DonationAlert deserialization"""
        alert_data = {
            'amount': 100.00,
            'address': 'S8f3test1234567890abcdef',
            'timestamp': 1234567890.123
        }
        
        alert = DonationAlert.from_dict(alert_data)
        
        self.assertEqual(alert.amount, alert_data['amount'])
        self.assertEqual(alert.address, alert_data['address'])
        self.assertEqual(alert.timestamp, alert_data['timestamp'])

def run_unit_tests():
    """Run all unit tests"""
    print("🧪 Running Unit Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSatoxWalletMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestDonationAlert))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if not result.failures and not result.errors:
        print("\n✅ All unit tests passed!")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_unit_tests()
    sys.exit(0 if success else 1) 