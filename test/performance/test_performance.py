#!/usr/bin/env python3
"""
Performance Tests for Satoxcoin Stream Donation Overlay
Benchmarks various components and operations
"""

import unittest
import sys
import os
import time
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

class TestPerformance(unittest.TestCase):
    """Performance tests for the donation monitoring system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            'wallet_address': 'S8f3test1234567890abcdef',
            'rpc_url': 'http://localhost:8332',
            'check_interval': 30,
            'alert_duration': 5,
            'log_file': 'test_performance.log'
        }
        self.monitor = SatoxWalletMonitor(self.test_config)
    
    def test_address_obfuscation_performance(self):
        """Test performance of address obfuscation"""
        test_address = "S8f3test1234567890abcdef"
        iterations = 10000
        
        start_time = time.time()
        for _ in range(iterations):
            obfuscated = self.monitor.obfuscate_address(test_address)
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_second = iterations / duration
        
        print(f"Address obfuscation: {ops_per_second:.0f} ops/sec")
        self.assertGreater(ops_per_second, 1000)  # Should be very fast
    
    def test_alert_creation_performance(self):
        """Test performance of alert creation"""
        iterations = 1000
        
        start_time = time.time()
        alerts = []
        for i in range(iterations):
            alert = DonationAlert(amount=float(i), address=f"S8f3test{i:06d}")
            alerts.append(alert)
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_second = iterations / duration
        
        print(f"Alert creation: {ops_per_second:.0f} ops/sec")
        self.assertGreater(ops_per_second, 100)  # Should be reasonably fast
    
    def test_alert_serialization_performance(self):
        """Test performance of alert serialization"""
        alert = DonationAlert(amount=150.0, address="S8f3test1234567890abcdef")
        iterations = 10000
        
        start_time = time.time()
        for _ in range(iterations):
            data = alert.to_dict()
            json_str = json.dumps(data)
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_second = iterations / duration
        
        print(f"Alert serialization: {ops_per_second:.0f} ops/sec")
        self.assertGreater(ops_per_second, 1000)  # Should be very fast
    
    def test_file_write_performance(self):
        """Test performance of alert file writing"""
        iterations = 100
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            start_time = time.time()
            for i in range(iterations):
                message = f"Test donation {i}: 150.00 SATOX"
                with open(temp_filename, 'w') as f:
                    f.write(message)
            end_time = time.time()
            
            duration = end_time - start_time
            ops_per_second = iterations / duration
            
            print(f"File write performance: {ops_per_second:.0f} ops/sec")
            self.assertGreater(ops_per_second, 10)  # Should be reasonably fast
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_rpc_call_performance(self):
        """Test performance of RPC calls (mocked)"""
        iterations = 100
        
        # Mock the RPC response
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': 150.75,
            'error': None
        }
        mock_response.status_code = 200
        
        with patch('requests.post', return_value=mock_response):
            start_time = time.time()
            for _ in range(iterations):
                result = self.monitor.rpc_call('getbalance')
            end_time = time.time()
            
            duration = end_time - start_time
            ops_per_second = iterations / duration
            
            print(f"RPC call performance (mocked): {ops_per_second:.0f} ops/sec")
            self.assertGreater(ops_per_second, 50)  # Should be reasonably fast
    
    def test_memory_usage(self):
        """Test memory usage with many alerts"""
        alerts = []
        iterations = 10000
        
        # Create many alerts
        for i in range(iterations):
            alert = DonationAlert(amount=float(i), address=f"S8f3test{i:06d}")
            alerts.append(alert)
        
        # Check that we can still process them
        start_time = time.time()
        for alert in alerts:
            data = alert.to_dict()
            _ = json.dumps(data)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Processed {iterations} alerts in {duration:.2f} seconds")
        self.assertLess(duration, 5.0)  # Should complete within 5 seconds

def run_performance_tests():
    """Run all performance tests"""
    print("🚀 Running Performance Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformance)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All performance tests passed!")
        return True
    else:
        print("❌ Some performance tests failed!")
        return False

if __name__ == "__main__":
    success = run_performance_tests()
    sys.exit(0 if success else 1) 