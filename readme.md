# QuickBuy Pro - One-Click Purchase Automation

**Author:** [flenco.in](https://flenco.in)
**Support:** [Buy me a coffee](https://buymeacoffee.com/atishpaul)

## Features

- **One-Click Purchase** - Automate complete purchase flow
- **Smart Login Detection** - Auto-detects login status
- **Custom Card Details** - Use your own card details or default test cards
- **Schedule Execution** - Execute now or schedule for later
- **Persistent Scheduling** - Schedules survive app restarts
- **Smart Error Handling** - Skips problematic steps automatically
- **User-Friendly Interface** - Clear step-by-step progress
- **Cross-Platform Support** - Works on Windows, macOS, and Linux
- **Self-Contained** - No external ChromeDriver downloads needed

## Quick Start

### Clone and Run
1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd one-click-buy-fk
   ```

2. **Run the Tool**
   
   **On Windows:**
   ```cmd
   run.bat
   ```
   
   **On macOS/Linux:**
   ```bash
   ./run.sh
   ```

   **Or run directly with Python:**
   ```bash
   python automation.py
   ```

### What's Included
- ✅ **Automatic ChromeDriver Management** - Downloads correct version automatically
- ✅ **Cross-Platform Support** - Works on Windows, macOS, and Linux
- ✅ **Automatic OS Detection** - Script detects your platform automatically
- ✅ **Minimal Dependencies** - Only requires Python and Selenium
- ✅ **User Data Persistence** - Login data saved locally
- ✅ **No Manual Setup** - Everything handled automatically

## How It Works

### Automation Steps:
1. **Login Detection** - Automatically detects if you're logged in
2. **Product Page** - Opens your selected product page
3. **Buy Now** - Clicks the Buy Now button
4. **Contact Info** - Handles contact information
5. **Payment Page** - Proceeds to payment section
6. **Accept & Continue** - Handles payment page popups
7. **Card Selection** - Selects credit card payment method
8. **Card Details** - Fills in card number, expiry, and CVV
9. **Final Payment** - Completes the purchase process

## Configuration

- **Product URL**: Select all product options before copying URL
- **Card Details**: Optional - uses test cards by default
- **Execution Time**: Choose immediate or scheduled execution
- **User Data**: Automatically saved for persistent login

## Security

- ✅ **Local Execution Only** - No data sent to external servers
- ✅ **Secure User Data Storage** - Login data stored locally
- ✅ **Test Card Support** - Safe testing with default test cards
- ✅ **No Sensitive Data Logging** - Card details not logged

## Usage Options

### Execute Now
Run automation immediately after login

### Schedule for Later
- Set date and time for execution
- Keep tool running for scheduled execution
- Cancel or modify scheduled executions

## System Requirements

- **Python**: 3.7 or later
- **Chrome Browser**: Must be installed and updated
- **Internet Connection**: Required for automation
- **Operating System**: Windows 10+, macOS 10.15+, or Linux

## Project Structure

```
quickbuy-pro/
├── automation.py               # Main automation script
├── requirements.txt            # Python dependencies
├── run.sh                      # Unix/macOS/Linux runner
├── run.bat                     # Windows runner
├── readme.md                   # This file
└── user_data/                  # User data storage (auto-created, ignored by git)
```

## Windows Compatibility

✅ **Fully Windows Compatible!** 

The script has been thoroughly tested for Windows compatibility:

- ✅ **Windows 10/11 Support** - Tested on latest Windows versions
- ✅ **Path Handling** - Proper Windows path handling (`C:\Users\...`)
- ✅ **Chrome Detection** - Finds Chrome in all standard Windows locations
- ✅ **WebDriver Manager** - Automatic ChromeDriver download for Windows
- ✅ **Batch File Runner** - `run.bat` for easy Windows execution

### Windows-Specific Features:
- **Multiple Chrome Paths**: Checks Program Files, Program Files (x86), and LocalAppData
- **Windows Path Support**: Handles both forward and backward slashes
- **Batch Script**: `run.bat` provides native Windows experience
- **Error Handling**: Windows-specific error messages and solutions

## Troubleshooting

- **ChromeDriver Issues**: The script automatically detects your OS and uses the correct ChromeDriver
- **Login Problems**: Make sure you're logged into Flipkart in your browser first
- **Product URL**: Ensure all product options (color, size, etc.) are selected before copying the URL
- **Dependencies**: Run `pip install -r requirements.txt` if you get import errors

## Support

- **Author**: flenco.in
- **Coffee**: https://buymeacoffee.com/atishpaul
- **Issues**: Report any bugs or feature requests

---

**Disclaimer**: This tool is for educational and testing purposes only. Use responsibly and in accordance with website terms of service.