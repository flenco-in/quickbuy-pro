# QuickBuy Pro - E-commerce Purchase Automation

**Author:** flenco.in
**Support:** https://buymeacoffee.com/atishpaul

## Overview

QuickBuy Pro automates the e-commerce purchase process using Selenium WebDriver. The tool provides automated purchasing capabilities with support for scheduling and persistent login management.

## Features

- Automated purchase flow execution
- Login status detection and management
- Optional card details pre-filling
- Scheduled execution with time-based triggers
- Cross-platform compatibility (Windows, macOS, Linux)
- Automatic ChromeDriver management

## Installation

### Prerequisites
- Python 3.7 or later
- Google Chrome browser
- Internet connection

### Quick Start

**Windows:**
```cmd
run.bat
```

**macOS/Linux:**
```bash
./run.sh
```

**Direct Python execution:**
```bash
python automation.py
```

## System Requirements

- **Python**: 3.7+
- **Chrome Browser**: Latest version recommended
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB free space

## Dependencies

The tool uses the following Python packages:
- selenium>=4.15.0
- webdriver-manager>=4.0.0
- psutil>=5.9.0

Dependencies are automatically installed via requirements.txt.

## Usage

1. Run the application using the appropriate script for your platform
2. Follow the on-screen prompts for login verification
3. Provide the product URL (ensure all product options are selected)
4. Choose execution timing (immediate or scheduled)
5. Optionally provide payment details for automation

## Configuration

### Product URL Setup
- Navigate to the product page
- Select all required options (size, color, variant)
- Copy the complete URL after selections

### Payment Details
- Card details can be pre-filled for automation
- Test card numbers are used by default if no details provided
- All payment information is processed locally

### Scheduling
- Executions can be scheduled for specific date/time
- Scheduled tasks persist across application restarts
- Multiple scheduling options available

## Security

- All data processing occurs locally
- No external data transmission
- User login data stored in local browser profile
- Payment details are not logged or stored

## Project Structure

```
quickbuy-pro/
├── automation.py      # Main automation script
├── requirements.txt   # Python dependencies
├── run.bat           # Windows launcher
├── run.sh            # Unix/Linux launcher
└── README.md         # Documentation
```

## Troubleshooting

**Chrome/ChromeDriver Issues:**
- Ensure Chrome browser is installed and updated
- ChromeDriver is managed automatically

**Login Problems:**
- Verify internet connection
- Clear browser cache if needed
- Ensure proper login credentials

**Execution Failures:**
- Check product URL validity
- Verify all product options are selected
- Ensure sufficient system resources

## Technical Details

- Built with Selenium WebDriver
- Automatic WebDriver management via webdriver-manager
- Cross-platform process management with psutil
- Chrome browser automation with custom options
- Local data persistence for user sessions

## Support

For issues, questions, or feature requests:
- Author: flenco.in
- Support: https://buymeacoffee.com/atishpaul

## Disclaimer

This software is provided for educational and testing purposes only. Users are responsible for compliance with all applicable terms of service and local regulations. Use at your own discretion and risk.

---

**Note:** This tool is designed for legitimate automation testing. Ensure compliance with website terms of service before use.