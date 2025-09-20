#!/bin/bash

# QuickBuy Pro - One-Click Purchase Automation
# Author: flenco.in
# Support: https://buymeacoffee.com/atishpaul

echo "=========================================="
echo "QuickBuy Pro - One-Click Purchase Automation"
echo "=========================================="
echo "Author: flenco.in"
echo "Support: https://buymeacoffee.com/atishpaul"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed. Please install Python 3.7 or later."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $PYTHON_CMD"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "❌ pip is not installed. Please install pip."
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "✅ pip found: $PIP_CMD"

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo ""
    echo "📦 Installing dependencies..."
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "⚠️  requirements.txt not found, skipping dependency installation"
fi

# Check if ChromeDriver exists locally for current platform
OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
    CHROMEDRIVER="chromedriver"
elif [ "$OS" = "Linux" ]; then
    CHROMEDRIVER="chromedriver-linux"
elif [ "$OS" = "CYGWIN" ] || [ "$OS" = "MINGW" ] || [ "$OS" = "MSYS" ]; then
    CHROMEDRIVER="chromedriver.exe"
else
    CHROMEDRIVER="chromedriver"
fi

if [ -f "$CHROMEDRIVER" ]; then
    echo "✅ Local ChromeDriver found: $CHROMEDRIVER"
    chmod +x "$CHROMEDRIVER"
else
    echo "⚠️  Local ChromeDriver not found for $OS, will use system ChromeDriver or webdriver-manager"
fi

echo ""
echo "🚀 Starting QuickBuy Pro..."
echo ""

# Run the automation script
$PYTHON_CMD flipkart_automation.py
