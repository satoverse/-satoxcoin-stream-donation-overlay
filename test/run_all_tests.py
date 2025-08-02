#!/usr/bin/env python3
"""
Comprehensive Test Runner for Satoxcoin Stream Donation Overlay
Runs all tests across all platforms and test types
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestRunner:
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def run_command(self, command: str, cwd: str = None) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out after 5 minutes"
        except Exception as e:
            return -1, "", str(e)
    
    def run_python_tests(self, test_path: str, test_name: str) -> Dict:
        """Run Python tests in a specific directory"""
        print(f"🧪 Running {test_name}...")
        
        # Try pytest first, then unittest
        exit_code, stdout, stderr = self.run_command(
            f"python3 -m pytest {test_path} -v --tb=short",
            cwd=os.path.join(os.path.dirname(__file__), '..')
        )
        
        if exit_code != 0:
            # Fallback to unittest
            exit_code, stdout, stderr = self.run_command(
                f"python3 -m unittest discover {test_path} -v",
                cwd=os.path.join(os.path.dirname(__file__), '..')
            )
        
        return {
            'exit_code': exit_code,
            'stdout': stdout,
            'stderr': stderr,
            'success': exit_code == 0
        }
    
    def run_shell_tests(self, test_path: str, test_name: str) -> Dict:
        """Run shell script tests"""
        print(f"🐚 Running {test_name}...")
        
        script_path = os.path.join(test_path, "test.sh")
        if os.path.exists(script_path):
            exit_code, stdout, stderr = self.run_command(
                f"bash {script_path}",
                cwd=test_path
            )
        else:
            return {
                'exit_code': 0,
                'stdout': f"No test script found in {test_path}",
                'stderr': '',
                'success': True
            }
        
        return {
            'exit_code': exit_code,
            'stdout': stdout,
            'stderr': stderr,
            'success': exit_code == 0
        }
    
    def run_unit_tests(self) -> Dict:
        """Run unit tests"""
        return self.run_python_tests("test/unit", "Unit Tests")
    
    def run_integration_tests(self) -> Dict:
        """Run integration tests"""
        return self.run_python_tests("test/integration", "Integration Tests")
    
    def run_e2e_tests(self) -> Dict:
        """Run end-to-end tests"""
        return self.run_python_tests("test/e2e", "End-to-End Tests")
    
    def run_performance_tests(self) -> Dict:
        """Run performance tests"""
        return self.run_python_tests("test/performance", "Performance Tests")
    
    def run_platform_tests(self) -> Dict:
        """Run platform-specific tests"""
        platform_results = {}
        platforms_dir = "test/platforms"
        
        if not os.path.exists(platforms_dir):
            return {'success': True, 'message': 'No platform tests found'}
        
        for platform in os.listdir(platforms_dir):
            platform_path = os.path.join(platforms_dir, platform)
            if os.path.isdir(platform_path):
                result = self.run_python_tests(platform_path, f"Platform Tests ({platform})")
                platform_results[platform] = result
        
        # Overall success if all platforms passed
        overall_success = all(result['success'] for result in platform_results.values())
        return {
            'success': overall_success,
            'platforms': platform_results
        }
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Test Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run each test suite
        test_suites = [
            ("Unit Tests", self.run_unit_tests),
            ("Integration Tests", self.run_integration_tests),
            ("End-to-End Tests", self.run_e2e_tests),
            ("Performance Tests", self.run_performance_tests),
            ("Platform Tests", self.run_platform_tests)
        ]
    
        for test_name, test_func in test_suites:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            self.test_results[test_name] = result
            
            if result['success']:
                print(f"✅ {test_name} PASSED")
                self.passed_tests += 1
            else:
                print(f"❌ {test_name} FAILED")
                if 'exit_code' in result:
                    print(f"Exit Code: {result['exit_code']}")
                if 'stderr' in result and result['stderr']:
                    print(f"Error: {result['stderr']}")
                if 'message' in result:
                    print(f"Message: {result['message']}")
                self.failed_tests += 1
            
            self.total_tests += 1
        
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Test Suites: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "N/A")
        print(f"Duration: {duration:.2f} seconds")
        print()
        
        if self.failed_tests > 0:
            print("❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result['success']:
                    print(f"  - {test_name}")
                    if 'platforms' in result:
                        for platform, platform_result in result['platforms'].items():
                            if not platform_result['success']:
                                print(f"    - {platform}")
        else:
            print("🎉 ALL TESTS PASSED!")
    
    def save_results(self):
        """Save test results to JSON file"""
        results_file = os.path.join(os.path.dirname(__file__), "test_results.json")
    
        # Clean up results for JSON serialization
        clean_results = {}
        for test_name, result in self.test_results.items():
            clean_results[test_name] = {
                'success': result['success'],
                'exit_code': result.get('exit_code', 0),
                'stdout': result.get('stdout', '')[:1000],  # Truncate long output
                'stderr': result.get('stderr', '')[:1000]
            }
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'success_rate': (self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0,
            'duration': time.time() - self.start_time,
            'results': clean_results
        }
        
        try:
            with open(results_file, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"📄 Results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")

def main():
    """Main entry point"""
    runner = TestRunner()
    runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(1 if runner.failed_tests > 0 else 0)

if __name__ == "__main__":
    main() 