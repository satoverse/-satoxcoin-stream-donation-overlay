# 🔧 Troubleshooting Guide - Satoxcoin Stream Donation Overlay

Comprehensive guide to resolve common issues and problems.

> **📚 Quick Navigation:** [Main README](../README.md) | [Installation Guide](INSTALLATION.md) | [Windows Guide](README-WINDOWS.md)

## 🚨 Common Issues

### 1. **Configuration Errors**

#### "RPC_USER not configured"
**Problem:** Placeholder values still in configuration
**Solution:**
```bash
# Option A: Set environment variables
export SATOX_RPC_USER="your_actual_username"
export SATOX_RPC_PASSWORD="your_actual_password"
export SATOX_DONATION_ADDRESS="your_actual_address"

# Option B: Edit wallet_monitor.py directly
# Replace placeholder values with real credentials
```

#### "Invalid donation address format"
**Problem:** Donation address doesn't match Satoxcoin format
**Solution:**
- Ensure address starts with 'S'
- Check address length (26-35 characters)
- Verify address is valid Satoxcoin address

### 2. **Connection Issues**

#### "Could not connect to Satox Core RPC"
**Problem:** Satox Core not running or RPC not enabled
**Solution:**
1. **Start Satox Core**
   ```bash
   # Start Satox Core wallet
   satox-qt
   # or
   satoxd
   ```

2. **Check satoxcoin.conf**
   ```ini
   server=1
   rpcuser=your_username
   rpcpassword=your_password
   rpcallowip=127.0.0.1
   rpcport=7777
   ```

3. **Test RPC connection**
   ```bash
   curl -u username:password http://127.0.0.1:7777
   ```

#### "RPC connection timed out"
**Problem:** Network or firewall blocking connection
**Solution:**
- Check firewall settings
- Verify port 7777 is open
- Ensure Satox Core is fully synced

### 3. **Python Issues**

#### "Python not found"
**Problem:** Python not installed or not in PATH
**Solution:**
```bash
# Install Python 3.7+
# Download from python.org
# Check "Add Python to PATH" during installation

# Verify installation
python --version
```

#### "Missing dependencies"
**Problem:** Required packages not installed
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install requests
```

### 4. **File Issues**

#### "Missing required files"
**Problem:** Project files not present
**Solution:**
```bash
# Check file structure
ls -la

# Ensure these files exist:
# - wallet_monitor.py
# - alert.html
# - demo.html
# - satox-logo.png
# - coin.mp3
# - requirements.txt
```

#### "Permission denied"
**Problem:** File permissions issues
**Solution:**
```bash
# Fix permissions (Linux/Mac)
chmod +x wallet_monitor.py
chmod +x validate_config.py

# Windows: Run as Administrator
```

### 5. **OBS Integration Issues**

#### "Overlay not showing"
**Problem:** Browser source not configured correctly
**Solution:**
1. **Check URL:** `http://localhost:8080/alert.html`
2. **Check dimensions:** Width 600, Height 300
3. **Enable audio capture** for sound effects
4. **Ensure web server is running**

#### "Sound not playing"
**Problem:** Audio not captured in OBS
**Solution:**
- Enable "Control audio via OBS" in browser source
- Check system audio settings
- Verify coin.mp3 file exists

### 6. **Web Server Issues**

#### "Port 8080 already in use"
**Problem:** Another service using the port
**Solution:**
```bash
# Find process using port 8080
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Linux/Mac

# Kill the process
taskkill /PID <process_id> /F  # Windows
kill <process_id>              # Linux/Mac
```

#### "Demo page not loading"
**Problem:** Web server not started
**Solution:**
```bash
# Start web server
python -m http.server 8080

# Visit in browser
http://localhost:8080/demo.html
```

## 🔍 Diagnostic Commands

### Check System Status
```bash
# Python version
python --version

# Dependencies
pip list | grep requests

# Network connectivity
ping 127.0.0.1

# Port availability
netstat -an | grep 8080
```

### Check Satox Core
```bash
# Test RPC connection
curl -u username:password http://127.0.0.1:7777

# Check Satox Core status
satox-cli getinfo
```

### Check Project Files
```bash
# Validate configuration
python validate_config.py

# Run quick setup
python quick_setup.py

# Check file permissions
ls -la *.py *.html *.png *.mp3
```

## 🛠️ Advanced Troubleshooting

### Debug Mode
Enable debug logging:
```bash
# Set environment variable
export SATOX_DEBUG=true

# Or edit wallet_monitor.py
DEBUG = True
```

### Log Analysis
Check log files for errors:
```bash
# Monitor logs in real-time
tail -f donation_monitor.log

# Check alert file
cat alert.txt
```

### Network Diagnostics
```bash
# Test localhost connectivity
telnet localhost 8080
telnet localhost 7777

# Check firewall rules
iptables -L  # Linux
netsh advfirewall show allprofiles  # Windows
```

## 📞 Getting Help

### Before Asking for Help
1. ✅ Run `python validate_config.py`
2. ✅ Check log files for errors
3. ✅ Test with demo page
4. ✅ Verify Satox Core is running
5. ✅ Check OBS browser source settings

### Information to Provide
- Operating system and version
- Python version
- Satox Core version
- Error messages from logs
- Steps to reproduce the issue

### Support Channels
- **GitHub Issues:** Create detailed issue report
- **Documentation:** Check README.md and this guide
- **Community:** Ask in Satoxcoin community channels

## 🎯 Quick Fixes

### Reset Configuration
```bash
# Remove generated files
rm -f alert.txt donation_monitor.log

# Reset to defaults
cp env.example .env
# Edit .env with your credentials
```

### Fresh Installation
```bash
# Clean install
rm -rf __pycache__/
pip uninstall requests
pip install -r requirements.txt
python quick_setup.py
```

### Test Everything
```bash
# Run all tests
python test_all.py

# Run validation
python validate_config.py

# Test demo
python -m http.server 8080
# Visit: http://localhost:8080/demo.html
```

## ✅ Success Checklist

- ✅ Python 3.7+ installed
- ✅ Dependencies installed
- ✅ Configuration validated
- ✅ Satox Core running and synced
- ✅ RPC connection working
- ✅ Web server running
- ✅ Demo page accessible
- ✅ OBS browser source configured
- ✅ Test donation triggers alert

If all items are checked, your setup should be working correctly! 🎉 