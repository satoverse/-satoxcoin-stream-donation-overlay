# 🚀 Installation Guide - Satoxcoin Stream Donation Overlay

Quick setup guide for the Satoxcoin donation overlay system.

> **📚 Quick Navigation:** [Main README](../README.md) | [Windows Guide](README-WINDOWS.md) | [Troubleshooting](TROUBLESHOOTING.md)

## 📋 Prerequisites

- **Python 3.7+** installed and added to PATH
- **Satox Core wallet** running with RPC enabled
- **OBS Studio** or **Streamlabs OBS** (or compatible streaming software)

## 🔧 Installation Steps

### 1. Download the Project
```bash
git clone https://github.com/satoverse/satoxcoin-stream-donation-overlay.git
cd satoxcoin-stream-donation-overlay
```

### 2. Install Dependencies
```bash
# Linux/Mac
pip3 install -r requirements.txt

# Windows
setup-windows.bat
```

### 3. Configure Satox Core RPC
Create `satoxcoin.conf` in your Satox data directory:
```ini
server=1
rpcuser=your_username
rpcpassword=your_rpc_password
rpcallowip=127.0.0.1
rpcport=7777
```

### 4. Configure the Monitor
Edit `wallet_monitor.py`:
```python
RPC_USER = "your_rpc_username"
RPC_PASSWORD = "your_rpc_password"
DONATION_ADDRESS = "your_donation_address_here"
MIN_DONATION = 1.0  # Minimum donation amount
```

### 5. Test the Setup
```bash
# Start demo server
python3 -m http.server 8080

# Visit: http://localhost:8080/demo.html
# Click "Test Donation" to verify everything works
```

### 6. Start Monitoring
```bash
# Linux/Mac
python3 wallet_monitor.py

# Windows
start-monitor.bat
```

### 7. Add to OBS
1. Add **Browser Source** in OBS
2. URL: `http://localhost:8080/alert.html`
3. Width: 600px, Height: 300px
4. Enable "Control audio via OBS" (optional)

## 🪟 Windows Quick Setup

1. **Extract** to `C:\satoxcoin-stream-donation-overlay\`
2. **Double-click** `setup-windows.bat`
3. **Edit** `wallet_monitor.py` with your settings
4. **Double-click** `start-demo.bat` to test
5. **Double-click** `start-monitor.bat` to begin monitoring

## 🔍 Troubleshooting

### Common Issues

**Python not found**
- Reinstall Python with "Add to PATH" checked
- Verify: `python --version`

**RPC connection failed**
- Check `satoxcoin.conf` settings
- Verify Satox Core is running
- Test: `curl -u username:password http://127.0.0.1:7777`

**Port already in use**
```bash
# Kill existing process
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

### Log Files
- `donation_monitor.log` - Detailed monitoring logs
- `alert.txt` - Current alert message

## 📊 Satoxcoin Network Info

- **RPC Port:** 7777
- **P2P Port:** 60777
- **Algorithm:** KawPoW
- **Block Time:** 60 seconds

## 🔒 Security Notes

1. **Create a dedicated donation wallet**
2. **Use strong RPC passwords**
3. **Restrict RPC to localhost only**
4. **Regular wallet backups**

## 📚 More Information

- **Full Documentation:** [README.md](README.md)
- **Repository:** [https://github.com/satoverse/satoxcoin-stream-donation-overlay](https://github.com/satoverse/satoxcoin-stream-donation-overlay)
- **Satoxcoin:** [https://github.com/satoverse/satoxcoin](https://github.com/satoverse/satoxcoin)

## Copyright

**Copyright (c) 2025 Satoxcoin Core Developers**

## License

This project is open source and available under the MIT License.

---

**Ready to stream with Satoxcoin donations! 🚀💰** 