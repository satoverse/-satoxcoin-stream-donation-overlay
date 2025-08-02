#!/usr/bin/env python3
"""
End-to-End Tests for Satoxcoin Stream Donation Overlay
Tests the complete system workflow from donation to overlay display
"""

import unittest
import sys
import os
import time
import subprocess
import requests
import json
import threading
from pathlib import Path
from unittest.mock import patch, Mock

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end workflow tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.test_port = 8080
        self.server_process = None
        self.monitor_process = None
    
    def tearDown(self):
        """Clean up after tests"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        
        if self.monitor_process:
            self.monitor_process.terminate()
            self.monitor_process.wait()
    
    def test_complete_donation_workflow(self):
        """Test the complete donation workflow from start to finish"""
        try:
            # Start the web server
            self.server_process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(self.test_port)],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Test 1: Verify server is running
            response = requests.get(f'http://localhost:{self.test_port}/', timeout=5)
            self.assertEqual(response.status_code, 200)
            
            # Test 2: Verify overlay files are accessible
            response = requests.get(f'http://localhost:{self.test_port}/alert.html', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('satox-logo.png', response.text)
            
            # Test 3: Verify demo page works
            response = requests.get(f'http://localhost:{self.test_port}/demo.html', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Satoxcoin', response.text)
            
            # Test 4: Verify assets are accessible
            response = requests.get(f'http://localhost:{self.test_port}/satox-logo.png', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('image/png', response.headers.get('content-type', ''))
            
            response = requests.get(f'http://localhost:{self.test_port}/coin.mp3', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('audio/mpeg', response.headers.get('content-type', ''))
            
        except requests.exceptions.RequestException as e:
            self.fail(f"End-to-end workflow test failed: {e}")
        except Exception as e:
            self.fail(f"End-to-end test setup failed: {e}")
    
    def test_wallet_monitor_integration(self):
        """Test wallet monitor integration with the overlay system"""
        # Test that wallet monitor can be imported and initialized
        try:
            from wallet_monitor import SatoxWalletMonitor
            
            config = {
                'wallet_address': 'S8f3test1234567890abcdef',
                'rpc_url': 'http://localhost:8332',
                'check_interval': 30,
                'alert_duration': 5,
                'log_file': 'test_e2e_monitor.log'
            }
            
            monitor = SatoxWalletMonitor(config)
            
            # Test basic functionality
            self.assertEqual(monitor.wallet_address, config['wallet_address'])
            self.assertEqual(monitor.rpc_url, config['rpc_url'])
            
            # Test address validation
            self.assertTrue(monitor.validate_address(config['wallet_address']))
            
            # Test address obfuscation
            obfuscated = monitor.obfuscate_address(config['wallet_address'])
            self.assertIn('****', obfuscated)
            
        except ImportError as e:
            self.fail(f"Could not import wallet monitor: {e}")
        except Exception as e:
            self.fail(f"Wallet monitor integration test failed: {e}")
    
    def test_overlay_customization(self):
        """Test that overlay customization works end-to-end"""
        try:
            # Start the web server
            self.server_process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(self.test_port)],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Test CSS variables are present and functional
            response = requests.get(f'http://localhost:{self.test_port}/alert.html', timeout=5)
            content = response.text
            
            # Check for CSS variables
            css_vars = [
                '--overlay-width',
                '--overlay-height',
                '--logo-size',
                '--alert-duration',
                '--primary-color',
                '--secondary-color',
                '--background-color'
            ]
            
            for var in css_vars:
                self.assertIn(var, content, f"CSS variable {var} not found in overlay")
            
            # Test JavaScript functionality
            response = requests.get(f'http://localhost:{self.test_port}/demo.html', timeout=5)
            content = response.text
            
            js_functions = [
                'playCoinSound',
                'showDonationAlert',
                'testDonation'
            ]
            
            for func in js_functions:
                self.assertIn(func, content, f"JavaScript function {func} not found in demo")
                
        except requests.exceptions.RequestException as e:
            self.fail(f"Overlay customization test failed: {e}")
        except Exception as e:
            self.fail(f"Overlay customization test setup failed: {e}")
    
    def test_multi_platform_compatibility(self):
        """Test that the overlay works across multiple platforms"""
        platforms = ['obs-studio', 'streamlabs-obs']
        
        for platform in platforms:
            platform_dir = self.base_dir / 'platforms' / platform
            assets_dir = platform_dir / 'assets'
            
            if assets_dir.exists():
                # Test platform-specific assets
                required_assets = ['alert.html', 'demo.html', 'satox-logo.png', 'coin.mp3']
                
                for asset in required_assets:
                    asset_path = assets_dir / asset
                    self.assertTrue(asset_path.exists(), f"Asset {asset} not found for {platform}")
                    
                    # Test file is readable
                    self.assertTrue(os.access(asset_path, os.R_OK), f"Asset {asset} not readable for {platform}")
    
    def test_error_handling(self):
        """Test error handling in the end-to-end system"""
        # Test with invalid wallet address
        try:
            from wallet_monitor import SatoxWalletMonitor
            
            config = {
                'wallet_address': 'invalid_address',
                'rpc_url': 'http://localhost:8332',
                'check_interval': 30,
                'alert_duration': 5,
                'log_file': 'test_error_handling.log'
            }
            
            monitor = SatoxWalletMonitor(config)
            
            # Should handle invalid address gracefully
            self.assertFalse(monitor.validate_address('invalid_address'))
            
        except ImportError:
            self.skipTest("Wallet monitor not available")
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")
    
    def test_performance_under_load(self):
        """Test system performance under simulated load"""
        try:
            # Start the web server
            self.server_process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(self.test_port)],
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Simulate multiple concurrent requests
            def make_request():
                try:
                    response = requests.get(f'http://localhost:{self.test_port}/alert.html', timeout=5)
                    return response.status_code == 200
                except:
                    return False
            
            # Create multiple threads to simulate concurrent users
            threads = []
            results = []
            
            for i in range(5):  # Simulate 5 concurrent users
                thread = threading.Thread(target=lambda: results.append(make_request()))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Check that all requests succeeded
            successful_requests = sum(results)
            self.assertGreaterEqual(successful_requests, 4, "System should handle concurrent requests")
            
        except Exception as e:
            self.fail(f"Performance test failed: {e}")

class TestProductionReadiness(unittest.TestCase):
    """Test production readiness of the system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent
    
    def test_production_file_structure(self):
        """Test that all production files are in place"""
        required_files = [
            'alert.html',
            'demo.html',
            'satox-logo.png',
            'coin.mp3',
            'wallet_monitor.py',
            'test_all.py',
            'requirements.txt',
            'README.md'
        ]
        
        for file_name in required_files:
            file_path = self.base_dir / file_name
            self.assertTrue(file_path.exists(), f"Production file {file_name} not found")
            
            # Check file permissions
            self.assertTrue(os.access(file_path, os.R_OK), f"Production file {file_name} not readable")
    
    def test_production_platform_structure(self):
        """Test that all platform directories are properly structured"""
        platforms = [
            'obs-studio',
            'streamlabs-obs'
        ]
        
        for platform in platforms:
            platform_dir = self.base_dir / 'platforms' / platform
            
            # Check platform directory exists
            self.assertTrue(platform_dir.exists(), f"Platform directory {platform} not found")
            
            # Check assets directory
            assets_dir = platform_dir / 'assets'
            self.assertTrue(assets_dir.exists(), f"Assets directory not found for {platform}")
            
            # Check README exists
            readme_file = platform_dir / 'README.md'
            self.assertTrue(readme_file.exists(), f"README not found for {platform}")
            
            # Check scripts directory
            scripts_dir = platform_dir / 'scripts'
            self.assertTrue(scripts_dir.exists(), f"Scripts directory not found for {platform}")
    
    def test_production_documentation(self):
        """Test that all documentation is complete"""
        doc_files = [
            'README.md',
            'INSTALLATION-GUIDE.md'
        ]
        
        for doc_file in doc_files:
            file_path = self.base_dir / doc_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check for minimum content length
                    self.assertGreater(len(content), 1000, f"Documentation {doc_file} is too short")
                    
                    # Check for key sections
                    key_sections = ['Installation', 'Usage', 'Configuration']
                    for section in key_sections:
                        if section.lower() in content.lower():
                            break
                    else:
                        self.fail(f"Documentation {doc_file} missing key sections")
    
    def test_production_security(self):
        """Test production security measures"""
        # Check that no real sensitive information is exposed
        # Allow placeholder values but check for real credentials
        sensitive_patterns = [
            'your_actual_password',
            'your_actual_username',
            'your_actual_address',
            'secret_key',
            'private_key',
            'api_key'
        ]
        
        # Check main files for sensitive information
        main_files = ['wallet_monitor.py', 'alert.html', 'demo.html']
        
        for file_name in main_files:
            file_path = self.base_dir / file_name
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                    for pattern in sensitive_patterns:
                        self.assertNotIn(pattern, content, f"Sensitive pattern '{pattern}' found in {file_name}")

def run_e2e_tests():
    """Run all end-to-end tests"""
    print("🔄 Running End-to-End Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionReadiness))
    
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
        print("\n✅ All end-to-end tests passed!")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_e2e_tests()
    sys.exit(0 if success else 1) 