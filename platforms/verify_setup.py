#!/usr/bin/env python3
"""
Satoxcoin Donation Overlay - Complete Verification Script
Tests both OBS Studio and Streamlabs OBS setups
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(platform, test_script):
    """Run test script for a specific platform"""
    print(f"\n🧪 Testing {platform}...")
    print("=" * 50)
    
    try:
        # Get the absolute path to the test script
        script_path = Path(test_script).resolve()
        script_dir = script_path.parent
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def check_demo_files():
    """Check that demo files exist and are accessible"""
    print("\n🎬 Checking demo files...")
    
    platforms = ['obs-studio', 'streamlabs-obs']
    demo_files = []
    
    for platform in platforms:
        demo_path = Path(platform) / 'assets' / 'demo.html'
        if demo_path.exists():
            demo_files.append(f"✅ {platform}/assets/demo.html")
        else:
            demo_files.append(f"❌ {platform}/assets/demo.html (missing)")
    
    for file in demo_files:
        print(f"  {file}")
    
    return all("✅" in file for file in demo_files)

def check_alert_files():
    """Check that alert files exist and are accessible"""
    print("\n🔔 Checking alert files...")
    
    platforms = ['obs-studio', 'streamlabs-obs']
    alert_files = []
    
    for platform in platforms:
        alert_path = Path(platform) / 'assets' / 'alert.html'
        if alert_path.exists():
            alert_files.append(f"✅ {platform}/assets/alert.html")
        else:
            alert_files.append(f"❌ {platform}/assets/alert.html (missing)")
    
    for file in alert_files:
        print(f"  {file}")
    
    return all("✅" in file for file in alert_files)

def check_assets():
    """Check that all required assets exist"""
    print("\n🎨 Checking assets...")
    
    platforms = ['obs-studio', 'streamlabs-obs']
    missing_assets = []
    
    for platform in platforms:
        assets_dir = Path(platform) / 'assets'
        required_files = ['satox-logo.png', 'coin.mp3']
        
        for file in required_files:
            file_path = assets_dir / file
            if file_path.exists():
                print(f"  ✅ {platform}/assets/{file}")
            else:
                print(f"  ❌ {platform}/assets/{file} (missing)")
                missing_assets.append(f"{platform}/assets/{file}")
    
    return len(missing_assets) == 0

def main():
    """Main verification function"""
    print("🚀 Satoxcoin Donation Overlay - Complete Verification")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('obs-studio').exists() or not Path('streamlabs-obs').exists():
        print("❌ Error: Please run this script from the platforms directory")
        print("   Current directory should contain obs-studio/ and streamlabs-obs/ folders")
        return False
    
    # Run platform tests
    obs_passed = run_test("OBS Studio", "obs-studio/scripts/test_all_obs.py")
    streamlabs_passed = run_test("Streamlabs OBS", "streamlabs-obs/scripts/test_all_streamlabs.py")
    
    # Check demo files
    demo_ok = check_demo_files()
    
    # Check alert files
    alert_ok = check_alert_files()
    
    # Check assets
    assets_ok = check_assets()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    results = [
        ("OBS Studio Tests", obs_passed),
        ("Streamlabs OBS Tests", streamlabs_passed),
        ("Demo Files", demo_ok),
        ("Alert Files", alert_ok),
        ("Assets", assets_ok)
    ]
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("✅ Your donation overlay is ready to use!")
        print("\n📋 Next Steps:")
        print("1. Configure wallet_monitor.py with your Satox Core credentials")
        print("2. Add alert.html as Browser Source in OBS Studio or Streamlabs OBS")
        print("3. Test with a real donation to your address")
        return True
    else:
        print(f"⚠️  {total - passed} VERIFICATION(S) FAILED")
        print("❌ Please fix the issues above before using the overlay")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 