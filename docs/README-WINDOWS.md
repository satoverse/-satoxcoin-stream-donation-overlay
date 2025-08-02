# 🪟 Windows Setup Guide - Satoxcoin Stream Donation Overlay

Complete setup guide for Windows users to get the Satoxcoin donation overlay running.

> **📚 Quick Navigation:** [Main README](../README.md) | [Installation Guide](INSTALLATION.md) | [Troubleshooting](TROUBLESHOOTING.md)

## 🚀 Quick Windows Setup

### Step 1: Download and Extract
1. Download the project ZIP file
2. Extract to `%USERPROFILE%\Documents\satoxcoin-stream-donation-overlay\`
3. Open Command Prompt as Administrator

### Step 2: Run Setup Script
```cmd
cd "%USERPROFILE%\Documents\satoxcoin-stream-donation-overlay"
setup-windows.bat
```

This script will:
- ✅ Check Python installation
- ✅ Install required dependencies
- ✅ Verify all files are present
- ✅ Test the setup

### Step 3: Configure Your Settings
Edit `wallet_monitor.py` with your credentials:
```python
RPC_USER = "your_actual_username"
RPC_PASSWORD = "your_actual_password"
DONATION_ADDRESS = "your_actual_donation_address"
```

### Step 4: Test the Setup
```cmd
start-demo.bat
```
Then visit: `http://localhost:8080/demo.html`

### Step 5: Start Monitoring
```cmd
start-monitor.bat
```

## 🔧 Detailed Windows Configuration

### Python Installation
- **Download Python 3.7+** from [python.org](https://python.org)
- **Important:** Check "Add Python to PATH" during installation
- **Verify:** Open Command Prompt and type `python --version`

### Satox Core Setup
1. **Install Satox Core** from [satoxcoin.org](https://satoxcoin.org)
2. **Create `satoxcoin.conf`** in your Satox data directory:
   ```ini
   server=1
   rpcuser=your_username
   rpcpassword=your_password
   rpcallowip=127.0.0.1
   rpcport=7777
   ```
3. **Start Satox Core** and wait for it to sync

### Environment Variables (Optional)
Create a `.env` file in the project directory:
```
SATOX_RPC_USER=your_username
SATOX_RPC_PASSWORD=your_password
SATOX_DONATION_ADDRESS=your_address
SATOX_MIN_DONATION=1.0
SATOX_DEBUG=false
```

## 🎮 OBS Studio Integration

### Add Browser Source
1. **Open OBS Studio**
2. **Add Source** → **Browser**
3. **Settings:**
   - URL: `http://localhost:8080/alert.html`
   - Width: 600
   - Height: 300
   - Check "Control audio via OBS"

### Test the Overlay
1. **Start the monitor:** `start-monitor.bat`
2. **Send a test donation** to your address
3. **Watch for the alert** in OBS

## 🛠️ Windows Batch Scripts

### Available Scripts
- **`setup-windows.bat`** - Initial setup and dependency installation
- **`check-deps.bat`** - Check/install missing dependencies
- **`start-monitor.bat`** - Start donation monitoring
- **`start-demo.bat`** - Start local demo server
- **`install-service.bat`** - Install as Windows service (advanced)

### Running Scripts
```cmd
# Run any script by double-clicking or:
script-name.bat

# Or from Command Prompt:
call script-name.bat
```

## 🔍 Troubleshooting

### Common Windows Issues

**Python not found**
```cmd
# Reinstall Python with "Add to PATH" checked
# Or manually add to PATH:
set PATH=%PATH%;C:\Python39\
```

**Permission denied**
```cmd
# Run Command Prompt as Administrator
# Or check file permissions
```

**Port already in use**
```cmd
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process
taskkill /PID <process_id> /F
```

**RPC connection failed**
```cmd
# Test RPC connection
curl -u username:password http://127.0.0.1:7777

# Check satoxcoin.conf settings
# Ensure Satox Core is running
```

### Log Files
- **`donation_monitor.log`** - Detailed monitoring logs
- **`alert.txt`** - Current alert message
- **Check these files** for error details

### Windows Firewall
- **Allow Python** through Windows Firewall
- **Allow port 8080** for local web server
- **Allow port 7777** for Satox Core RPC

## 🔒 Security Notes

### Credential Management
- **Never commit** `.env` files to version control
- **Use strong passwords** for RPC authentication
- **Restrict RPC access** to localhost only
- **Regularly update** Satox Core

### Network Security
- **RPC is local only** - no external access needed
- **Web server is local** - only accessible from your machine
- **No data collection** - everything stays local

## 📞 Support

### Getting Help
1. **Check the logs** in `donation_monitor.log`
2. **Test with demo** using `start-demo.bat`
3. **Verify Satox Core** is running and synced
4. **Check OBS settings** and browser source configuration

### Useful Commands
```cmd
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Test RPC connection
curl -u username:password http://127.0.0.1:7777

# Check if port is in use
netstat -ano | findstr :8080
```

## 🎉 Success Checklist

- ✅ Python 3.7+ installed and in PATH
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Satox Core running with RPC enabled
- ✅ `satoxcoin.conf` configured correctly
- ✅ `wallet_monitor.py` configured with real credentials
- ✅ Demo server working (`http://localhost:8080/demo.html`)
- ✅ Monitor running without errors
- ✅ OBS browser source added and working
- ✅ Test donation triggers alert

Once all items are checked, your Satoxcoin donation overlay is ready for live streaming! 🚀 