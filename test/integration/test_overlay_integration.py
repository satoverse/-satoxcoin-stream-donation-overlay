#!/usr/bin/env python3
"""
Integration Tests for Satoxcoin Stream Donation Overlay
Tests the complete system integration
"""

import unittest
import sys
import os
import time
import subprocess
import requests
import json
from pathlib import Path
from unittest.mock import patch, Mock

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class TestOverlayIntegration(unittest.TestCase):
    """Integration tests for the overlay system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.assets_dir = self.base_dir / 'assets'
        self.scripts_dir = self.base_dir / 'scripts'
        self.test_port = 8080
        self.server_process = None
    
    def tearDown(self):
        """Clean up after tests"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    def test_required_files_exist(self):
        """Test that all required files exist"""
        required_files = [
            'alert.html',
            'demo.html',
            'satox-logo.png',
            'coin.mp3',
            'wallet_monitor.py',
            'test_all.py',
            'requirements.txt'
        ]
        
        for file_name in required_files:
            file_path = self.base_dir / file_name
            self.assertTrue(file_path.exists(), f"Required file {file_name} not found")
    
    def test_html_files_valid(self):
        """Test that HTML files are valid"""
        html_files = ['alert.html', 'demo.html']
        
        for html_file in html_files:
            file_path = self.base_dir / html_file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for basic HTML structure
                self.assertIn('<!doctype html>', content.lower())
                self.assertIn('<html', content.lower())
                self.assertIn('</html>', content.lower())
                
                # Check for required elements
                self.assertIn('satox-logo.png', content)
                self.assertIn('coin.mp3', content)
    
    def test_audio_file_valid(self):
        """Test that audio file is valid"""
        audio_file = self.base_dir / 'coin.mp3'
        self.assertTrue(audio_file.exists())
        self.assertGreater(audio_file.stat().st_size, 1000)  # Should be at least 1KB
    
    def test_image_file_valid(self):
        """Test that image file is valid"""
        image_file = self.base_dir / 'satox-logo.png'
        self.assertTrue(image_file.exists())
        self.assertGreater(image_file.stat().st_size, 1000)  # Should be at least 1KB
    
    def test_python_script_syntax(self):
        """Test that Python scripts have valid syntax"""
        python_files = ['wallet_monitor.py', 'test_all.py']
        
        for py_file in python_files:
            file_path = self.base_dir / py_file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
            except SyntaxError as e:
                self.fail(f"Syntax error in {py_file}: {e}")
    
    def test_web_server_startup(self):
        """Test that web server can start and serve files"""
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
            
            # Test server response
            response = requests.get(f'http://localhost:{self.test_port}/', timeout=5)
            self.assertEqual(response.status_code, 200)
            
            # Test demo page
            response = requests.get(f'http://localhost:{self.test_port}/demo.html', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Satoxcoin', response.text)
            
            # Test alert page
            response = requests.get(f'http://localhost:{self.test_port}/alert.html', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('satox-logo.png', response.text)
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Web server test failed: {e}")
        except Exception as e:
            self.fail(f"Server startup failed: {e}")
    
    def test_overlay_assets_loading(self):
        """Test that overlay assets load correctly"""
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
            
            # Test logo loading
            response = requests.get(f'http://localhost:{self.test_port}/satox-logo.png', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('image/png', response.headers.get('content-type', ''))
            
            # Test audio loading
            response = requests.get(f'http://localhost:{self.test_port}/coin.mp3', timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('audio/mpeg', response.headers.get('content-type', ''))
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Asset loading test failed: {e}")
        except Exception as e:
            self.fail(f"Asset test failed: {e}")
    
    def test_css_variables_present(self):
        """Test that CSS variables are defined for customization"""
        alert_file = self.base_dir / 'alert.html'
        
        with open(alert_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for CSS variables
            required_vars = [
                '--overlay-width',
                '--overlay-height',
                '--logo-size',
                '--alert-duration'
            ]
            
            for var in required_vars:
                self.assertIn(var, content, f"CSS variable {var} not found in alert.html")
    
    def test_javascript_functionality(self):
        """Test that JavaScript functions are present"""
        demo_file = self.base_dir / 'demo.html'
        
        with open(demo_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for required JavaScript functions
            required_functions = [
                'playCoinSound',
                'showDonationAlert',
                'testDonation'
            ]
            
            for func in required_functions:
                self.assertIn(func, content, f"JavaScript function {func} not found in demo.html")

class TestPlatformCompatibility(unittest.TestCase):
    """Test platform-specific compatibility"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.platforms_dir = self.base_dir / 'platforms'
    
    def test_platform_directories_exist(self):
        """Test that all platform directories exist"""
        expected_platforms = [
            'obs-studio',
            'streamlabs-obs'
        ]
        
        for platform in expected_platforms:
            platform_dir = self.platforms_dir / platform
            self.assertTrue(platform_dir.exists(), f"Platform directory {platform} not found")
    
    def test_platform_readme_files(self):
        """Test that platform README files exist"""
        platforms = [
            'obs-studio',
            'streamlabs-obs'
        ]
        
        for platform in platforms:
            readme_file = self.platforms_dir / platform / 'README.md'
            self.assertTrue(readme_file.exists(), f"README.md not found for {platform}")
    
    def test_platform_assets_consistency(self):
        """Test that all platforms have consistent assets"""
        platforms = ['obs-studio', 'streamlabs-obs']  # Only test ready platforms
        
        for platform in platforms:
            platform_assets = self.platforms_dir / platform / 'assets'
            
            # Check that assets directory exists
            self.assertTrue(platform_assets.exists(), f"Assets directory not found for {platform}")
            
            # Check that all required assets are present
            required_assets = ['alert.html', 'demo.html', 'satox-logo.png', 'coin.mp3']
            
            for asset in required_assets:
                asset_file = platform_assets / asset
                self.assertTrue(asset_file.exists(), f"Asset {asset} not found for {platform}")

def run_integration_tests():
    """Run all integration tests"""
    print("🔗 Running Integration Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestOverlayIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatformCompatibility))
    
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
        print("\n✅ All integration tests passed!")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1) 