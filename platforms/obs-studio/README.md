# OBS Studio Integration

This directory contains the Satoxcoin donation overlay specifically configured for OBS Studio.

## Features

- **Real-time Donation Monitoring**: Monitors Satox Core wallet for incoming donations
- **Animated Alerts**: Beautiful animated overlay with Satoverse branding
- **Sound Effects**: Coin sound plays when donations are received
- **Customizable**: Easy to modify colors, sizes, and timing
- **Windows Compatible**: Full Windows support with batch scripts

## Setup Instructions

1. **Install OBS Studio** from [obsproject.com](https://obsproject.com/)

2. **Add Browser Source**:
   - In OBS Studio, add a new "Browser" source
   - Set the URL to: `file:///path/to/this/directory/alert.html`
   - Set width: 400, height: 200
   - Check "Shutdown source when not visible"

3. **Configure Wallet Monitor**:
   - Edit `wallet_monitor.py` with your Satox Core RPC credentials
   - Set your donation address
   - Run the monitor: `python3 wallet_monitor.py`

4. **Test the Setup**:
   - Open `demo.html` in a browser to see the overlay
   - Use the demo buttons to test different configurations

## Files

- `alert.html` - Main overlay file for OBS
- `demo.html` - Demo page for testing
- `coin.mp3` - Sound effect for donations
- `satox-logo.png` - Satoverse logo
- `wallet_monitor.py` - Python script to monitor donations

## Customization

The overlay can be customized by modifying CSS variables in `alert.html`:

```css
:root {
  --logo-width: 80px;        /* Logo size */
  --logo-height: 80px;
  --text-color: #fff;        /* Text color */
  --font-size: 36px;         /* Text size */
  --fade-duration: 7s;       /* How long alert shows */
}
```

## Troubleshooting

- **No alerts showing**: Check that `wallet_monitor.py` is running and connected to Satox Core
- **Sound not playing**: Ensure `coin.mp3` is in the same directory as `alert.html`
- **Overlay not visible**: Check OBS browser source settings and file paths

## Support

For issues and questions, please refer to the main project documentation or create an issue in the project repository. 