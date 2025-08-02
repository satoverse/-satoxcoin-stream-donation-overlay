# Satoxcoin Stream Donation Overlay

A production-ready donation overlay for OBS Studio and Streamlabs OBS that displays real-time Satoxcoin donation alerts during live streams.

## Supported Platforms

This overlay is specifically designed and tested for:

- **OBS Studio** - The most popular open-source streaming software
- **Streamlabs OBS** - The feature-rich streaming software with built-in tools

Both platforms use the same underlying technology (browser sources) and work seamlessly with the provided donation monitoring system.

## Features

- **Real-time Donation Monitoring**: Monitors Satox Core wallet for incoming donations
- **Animated Alerts**: Beautiful animated overlay with Satoverse branding
- **Sound Effects**: Coin sound plays when donations are received
- **Customizable**: Easy to modify colors, sizes, and timing
- **Windows Compatible**: Full Windows support with batch scripts

## Quick Start

### 1. Choose Your Platform
- **OBS Studio**: Use the `obs-studio/` directory
- **Streamlabs OBS**: Use the `streamlabs-obs/` directory

### 2. Setup Instructions
Both platforms follow the same setup process:

1. **Install your streaming software**:
   - OBS Studio: [obsproject.com](https://obsproject.com/)
   - Streamlabs OBS: [streamlabs.com](https://streamlabs.com/)

2. **Add Browser Source**:
   - Add a new "Browser" source
   - Set the URL to: `file:///path/to/satoxcoin-stream-donation-overlay/alert.html`
   - Set width: 600, height: 300
   - Enable audio capture for sound effects

3. **Configure Wallet Monitor**:
   - Edit `wallet_monitor.py` with your Satox Core RPC credentials:
     ```python
     RPC_USER = "your_rpc_username"
     RPC_PASSWORD = "your_rpc_password"
     DONATION_ADDRESS = "your_donation_address_here"
     ```
   - Run the monitor: `python3 wallet_monitor.py`

4. **Test the Setup**:
   - Open `demo.html` in a browser to see the overlay
   - Use the demo buttons to test different configurations

## Directory Structure

```
satoxcoin-stream-donation-overlay/
├── platforms/
│   ├── obs-studio/           # OBS Studio integration
│   │   ├── assets/          # Overlay files
│   │   └── scripts/         # Python monitoring scripts
│   └── streamlabs-obs/      # Streamlabs OBS integration
│       ├── assets/          # Overlay files
│       └── scripts/         # Python monitoring scripts
├── wallet_monitor.py         # Main monitoring script
├── alert.html               # OBS overlay file
├── demo.html                # Demo/test page
└── README.md                # Main documentation
```

## Why These Platforms?

OBS Studio and Streamlabs OBS are chosen because they:

- **Use the same technology**: Both support browser sources with local file paths
- **Have proven reliability**: Millions of streamers use these platforms
- **Support local files**: No web hosting required
- **Have excellent audio support**: Direct audio capture from browser sources
- **Are actively maintained**: Regular updates and community support

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
- **Sound not playing**: Ensure audio capture is enabled in your streaming software
- **Overlay not visible**: Check browser source settings and file paths

## Repository

This project is hosted at: [https://github.com/satoverse/satoxcoin-stream-donation-overlay](https://github.com/satoverse/satoxcoin-stream-donation-overlay)

## Copyright

**Copyright (c) 2025 Satoxcoin Core Developers**

## License

This project is open source and available under the MIT License. 