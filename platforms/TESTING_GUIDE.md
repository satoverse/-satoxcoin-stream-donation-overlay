# Testing Guide - Verifying Your Donation Overlay

This guide will help you verify that your Satoxcoin donation overlay is working correctly for both OBS Studio and Streamlabs OBS.

## Quick Verification Steps

### 1. **Test the Demo Page**
```bash
# Navigate to your platform directory
cd obs-studio/  # or streamlabs-obs/

# Open demo.html in your browser
# This shows you exactly how the overlay will look
```

### 2. **Test the Python Script**
```bash
# Run the test script to check dependencies
python3 test_all_obs.py  # or test_all_streamlabs.py

# This should show all green checkmarks ✅
```

### 3. **Test the Wallet Monitor**
```bash
# Run the wallet monitor (after configuring it)
python3 wallet_monitor.py

# Should show: "Connected to Satox Core v[version]"
```

## Detailed Testing Process

### Step 1: Environment Check

#### Check Python Installation
```bash
python3 --version
# Should show Python 3.7 or higher
```

#### Check Dependencies
```bash
cd obs-studio/scripts/  # or streamlabs-obs/scripts/
python3 test_all_obs.py
```

**Expected Output:**
```
==================================================
Satoxcoin Twitch Donations - Python Test Suite
==================================================

[TEST] Python Installation...
✅ Python 3.9.5 installed

[TEST] Core Python Modules...
✅ All 7 core modules available

[TEST] Requests Module...
✅ requests 2.28.1 available

[TEST] Required Files...
✅ All 5 required files present

[TEST] Python Syntax...
✅ wallet_monitor.py syntax is valid

[TEST] Wallet Monitor Import...
✅ Module imports successfully with SatoxWalletMonitor class

==================================================
TEST RESULTS SUMMARY
==================================================
Tests Passed: 6
Tests Failed: 0
Total Tests: 6

🎉 ALL TESTS PASSED!
✅ Your setup is ready to use.
==================================================
```

### Step 2: Visual Testing

#### Test the Demo Page
1. Open `obs-studio/assets/demo.html` (or `streamlabs-obs/assets/demo.html`) in your browser
2. Click the "Test Alert" button
3. You should see:
   - Animated overlay appears
   - Sound plays (if enabled)
   - Logo bounces
   - Text fades in/out

#### Test Different Scenarios
- Try different donation amounts
- Test with long/short addresses
- Verify animations work smoothly

### Step 3: Wallet Connection Test

#### Configure the Monitor
1. Edit `wallet_monitor.py`:
```python
RPC_USER = "your_actual_username"
RPC_PASSWORD = "your_actual_password"
DONATION_ADDRESS = "your_donation_address_here"
```

#### Test Connection
```bash
python3 wallet_monitor.py
```

**Expected Output:**
```
2024-01-15 10:30:15 - INFO - Starting Satoxcoin donation monitor...
2024-01-15 10:30:15 - INFO - Monitoring address: S8f3x2a1b2c3d4e5f6...
2024-01-15 10:30:15 - INFO - Minimum donation: 100.0 SATOX
2024-01-15 10:30:15 - INFO - Alert file: /path/to/alert.txt
2024-01-15 10:30:15 - INFO - Connected to Satox Core v1.0.0
2024-01-15 10:30:15 - INFO - Monitor is running. Press Ctrl+C or 'q' to stop.
```

### Step 4: OBS/Streamlabs Integration Test

#### Add Browser Source
1. Open OBS Studio or Streamlabs OBS
2. Add a new "Browser" source
3. Set URL to: `file:///path/to/obs-studio/assets/alert.html`
4. Set width: 400, height: 200
5. Enable "Shutdown source when not visible"

#### Test in Streaming Software
1. Start the wallet monitor: `python3 wallet_monitor.py`
2. In OBS/Streamlabs, you should see the overlay
3. Send a test donation to your address
4. Verify the overlay appears with animation and sound

### Step 5: Real Donation Test

#### Send a Test Donation
1. Make sure your Satox Core wallet is running
2. Send a small donation (above MIN_DONATION) to your donation address
3. Watch the overlay in OBS/Streamlabs
4. Check the console output for confirmation

**Expected Console Output:**
```
2024-01-15 10:35:22 - INFO - New donation: 150.0 SATOX from S8f3x2a1...
2024-01-15 10:35:22 - DEBUG - Alert written: S8f3x2a1... donated 150.00 SATOX!
```

## Troubleshooting Common Issues

### Issue: "Python not found"
**Solution:**
```bash
# Install Python 3.7+ and add to PATH
# Or use: python --version (instead of python3)
```

### Issue: "Missing dependency: requests"
**Solution:**
```bash
pip3 install requests
# Or run: setup-windows.bat (on Windows)
```

### Issue: "Failed to connect to Satox Core"
**Solution:**
1. Make sure Satox Core is running
2. Check `satoxcoin.conf` settings
3. Verify RPC username/password
4. Check firewall settings

### Issue: "No alerts showing in OBS"
**Solution:**
1. Check that `wallet_monitor.py` is running
2. Verify browser source URL is correct
3. Check that `alert.txt` is being created
4. Ensure audio capture is enabled

### Issue: "Sound not playing"
**Solution:**
1. Check that `coin.mp3` exists in the assets folder
2. Enable "Capture audio from browser source" in OBS
3. Check browser audio permissions
4. Try refreshing the browser source

## Automated Testing Script

Create a test script to verify everything:

```bash
#!/bin/bash
echo "🧪 Testing Satoxcoin Donation Overlay..."

# Test Python
echo "1. Testing Python installation..."
python3 --version || { echo "❌ Python not found"; exit 1; }
echo "✅ Python OK"

# Test dependencies
echo "2. Testing dependencies..."
cd obs-studio/scripts/
python3 test_all_obs.py || { echo "❌ Dependencies failed"; exit 1; }
echo "✅ Dependencies OK"

# Test wallet connection
echo "3. Testing wallet connection..."
python3 wallet_monitor.py --test-only || { echo "❌ Wallet connection failed"; exit 1; }
echo "✅ Wallet connection OK"

echo "🎉 All tests passed! Your overlay is ready to use."
```

## Performance Testing

### Test Animation Performance
- Run multiple rapid donations
- Check for smooth animations
- Verify no memory leaks

### Test Audio Performance
- Test with different audio formats
- Check volume levels
- Verify no audio lag

### Test File I/O Performance
- Monitor `alert.txt` creation speed
- Check file permissions
- Verify no file corruption

## Security Testing

### Test RPC Security
- Verify RPC credentials are secure
- Check network access
- Test with wrong credentials

### Test File Security
- Check file permissions
- Verify no unauthorized access
- Test with corrupted files

## Final Verification Checklist

- [ ] Python 3.7+ installed
- [ ] All dependencies installed
- [ ] Satox Core wallet running
- [ ] RPC credentials configured
- [ ] Demo page works in browser
- [ ] Wallet monitor connects successfully
- [ ] Browser source added to OBS/Streamlabs
- [ ] Overlay visible in streaming software
- [ ] Test donation triggers overlay
- [ ] Sound plays correctly
- [ ] Animations work smoothly

If all items are checked, your donation overlay is working correctly! 🎉

## Copyright

**Copyright (c) 2025 Satoxcoin Core Developers**

## License

This project is open source and available under the MIT License. 