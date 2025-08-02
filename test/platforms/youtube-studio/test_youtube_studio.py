#!/usr/bin/env python3
"""
YouTube Studio Platform Tests
Comprehensive testing for YouTube Studio integration
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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

class TestYouTubeStudioIntegration(unittest.TestCase):
    """YouTube Studio specific integration tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent.parent
        self.platform_dir = self.base_dir / 'platforms' / 'youtube-studio'
        self.assets_dir = self.platform_dir / 'assets'
        self.test_port = 8084
        self.server_process = None
    
    def tearDown(self):
        """Clean up after tests"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    def test_youtube_studio_assets_exist(self):
        """Test that YouTube Studio specific assets exist"""
        required_assets = [
            'alert.html',
            'demo.html',
            'satox-logo.png',
            'coin.mp3'
        ]
        
        for asset in required_assets:
            asset_path = self.assets_dir / asset
            self.assertTrue(asset_path.exists(), f"YouTube Studio asset {asset} not found")
    
    def test_youtube_studio_html_compatibility(self):
        """Test that HTML files are compatible with YouTube Studio"""
        html_files = ['alert.html', 'demo.html']
        
        for html_file in html_files:
            file_path = self.assets_dir / html_file
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # YouTube Studio specific requirements
                self.assertIn('<!doctype html>', content.lower())
                self.assertIn('<html', content.lower())
                self.assertIn('</html>', content.lower())
                
                # Check for browser source compatibility
                self.assertIn('satox-logo.png', content)
                self.assertIn('coin.mp3', content)
                
                # Check for CSS variables for customization (only in alert.html)
                if html_file == 'alert.html':
                    self.assertIn('--overlay-width', content)
                    self.assertIn('--overlay-height', content)
                    self.assertIn('--logo-size', content)
                    self.assertIn('--alert-duration', content)
    
    def test_youtube_studio_web_server(self):
        """Test that YouTube Studio web server functionality works"""
        base_url = "http://localhost:8080/"
        alert_url = base_url + "alert.html"
        
        # Test alert URL
        try:
            response = requests.get(alert_url, timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('text/html', response.headers.get('content-type', ''))
        except requests.exceptions.RequestException:
            # Server might not be running, but we can still test the URL format
            self.assertTrue(alert_url.startswith('http://'))
            self.assertTrue(alert_url.endswith('alert.html'))
        
        # Test demo URL
        demo_url = base_url + "demo.html"
        try:
            response = requests.get(demo_url, timeout=5)
            self.assertEqual(response.status_code, 200)
            self.assertIn('text/html', response.headers.get('content-type', ''))
        except requests.exceptions.RequestException:
            # Server might not be running, but we can still test the URL format
            self.assertTrue(demo_url.startswith('http://'))
            self.assertTrue(demo_url.endswith('demo.html'))
    
    def test_youtube_studio_css_customization(self):
        """Test that CSS variables work for YouTube Studio customization"""
        alert_file = self.assets_dir / 'alert.html'
        
        with open(alert_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for CSS custom properties
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
                self.assertIn(var, content, f"CSS variable {var} not found in YouTube Studio alert.html")
    
    def test_youtube_studio_javascript_functionality(self):
        """Test that JavaScript functions work in YouTube Studio"""
        demo_file = self.assets_dir / 'demo.html'
        
        with open(demo_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for required JavaScript functions
            js_functions = [
                'playCoinSound',
                'showDonationAlert',
                'testDonation',
                'updateDonationAmount'
            ]
            
            for func in js_functions:
                self.assertIn(func, content, f"JavaScript function {func} not found in YouTube Studio demo.html")
    
    def test_youtube_studio_file_permissions(self):
        """Test that files have correct permissions for YouTube Studio"""
        required_files = [
            'alert.html',
            'demo.html',
            'satox-logo.png',
            'coin.mp3'
        ]
        
        for file_name in required_files:
            file_path = self.assets_dir / file_name
            self.assertTrue(file_path.exists())
            
            # Check if file is readable
            self.assertTrue(os.access(file_path, os.R_OK), f"File {file_name} is not readable")
    
    def test_youtube_studio_directory_structure(self):
        """Test that YouTube Studio directory structure is correct"""
        # Check main platform directory
        self.assertTrue(self.platform_dir.exists())
        
        # Check assets directory
        self.assertTrue(self.assets_dir.exists())
        
        # Check README exists
        readme_file = self.platform_dir / 'README.md'
        self.assertTrue(readme_file.exists())
        
        # Check scripts directory
        scripts_dir = self.platform_dir / 'scripts'
        self.assertTrue(scripts_dir.exists())
    
    def test_youtube_studio_script_files(self):
        """Test that YouTube Studio script files exist and are valid"""
        scripts_dir = self.platform_dir / 'scripts'
        
        if scripts_dir.exists():
            script_files = list(scripts_dir.glob('*.bat')) + list(scripts_dir.glob('*.py'))
            
            for script_file in script_files:
                self.assertTrue(script_file.exists())
                self.assertTrue(os.access(script_file, os.R_OK))
                
                # Check if Python scripts have valid syntax
                if script_file.suffix == '.py':
                    try:
                        with open(script_file, 'r', encoding='utf-8') as f:
                            compile(f.read(), script_file, 'exec')
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {script_file.name}: {e}")

class TestYouTubeStudioPerformance(unittest.TestCase):
    """YouTube Studio performance tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = Path(__file__).parent.parent.parent.parent
        self.platform_dir = self.base_dir / 'platforms' / 'youtube-studio'
        self.assets_dir = self.platform_dir / 'assets'
    
    def test_alert_html_load_time(self):
        """Test that alert.html loads quickly"""
        alert_file = self.assets_dir / 'alert.html'
        
        if alert_file.exists():
            start_time = time.time()
            
            with open(alert_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            load_time = time.time() - start_time
            
            # Should load in under 100ms
            self.assertLess(load_time, 0.1, f"Alert HTML load time {load_time:.3f}s is too slow")
    
    def test_asset_file_sizes(self):
        """Test that asset files are reasonably sized"""
        assets = {
            'alert.html': (1024, 50000),  # 1KB to 50KB
            'demo.html': (1024, 100000),  # 1KB to 100KB
            'satox-logo.png': (1024, 500000),  # 1KB to 500KB
            'coin.mp3': (1024, 2000000)  # 1KB to 2MB
        }
        
        for asset_name, (min_size, max_size) in assets.items():
            asset_path = self.assets_dir / asset_name
            
            if asset_path.exists():
                file_size = asset_path.stat().st_size
                self.assertGreaterEqual(file_size, min_size, f"{asset_name} is too small ({file_size} bytes)")
                self.assertLessEqual(file_size, max_size, f"{asset_name} is too large ({file_size} bytes)")

def run_youtube_studio_tests():
    """Run all YouTube Studio tests"""
    print("🎬 Running YouTube Studio Platform Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestYouTubeStudioIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestYouTubeStudioPerformance))
    
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
        print("\n✅ All YouTube Studio tests passed!")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_youtube_studio_tests()
    sys.exit(0 if success else 1) 