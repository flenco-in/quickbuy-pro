#!/bin/bash

# QuickBuy Pro - One-Click Purchase Automation
# Author: flenco.in
# Support: https://buymeacoffee.com/atishpaul

set -e  # Exit on any error

echo "=========================================="
echo "QuickBuy Pro - One-Click Purchase Automation"
echo "=========================================="
echo "Author: flenco.in"
echo "Support: https://buymeacoffee.com/atishpaul"
echo "=========================================="
echo ""

# Function to check if Chrome is installed
check_chrome() {
    local chrome_found=false
    local chrome_path=""
    
    # Check common Chrome installation paths
    if [ "$OS" = "Darwin" ]; then
        if [ -d "/Applications/Google Chrome.app" ]; then
            chrome_found=true
            chrome_path="/Applications/Google Chrome.app"
        fi
    elif [ "$OS" = "Linux" ]; then
        if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
            chrome_found=true
        fi
    else
        # Windows
        if [ -f "/c/Program Files/Google/Chrome/Application/chrome.exe" ] || [ -f "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" ]; then
            chrome_found=true
        fi
    fi
    
    if [ "$chrome_found" = false ]; then
        echo "❌ Chrome browser not found!"
        echo ""
        echo "📥 Please install Google Chrome:"
        if [ "$OS" = "Darwin" ]; then
            echo "   • Visit: https://www.google.com/chrome/"
            echo "   • Or run: brew install --cask google-chrome"
        elif [ "$OS" = "Linux" ]; then
            echo "   • Ubuntu/Debian: sudo apt-get install google-chrome-stable"
            echo "   • Or visit: https://www.google.com/chrome/"
        else
            echo "   • Visit: https://www.google.com/chrome/"
        fi
        echo ""
        exit 1
    else
        echo "✅ Chrome browser found"
    fi
}

# Detect operating system
OS=$(uname -s)
echo "🖥️  Operating System: $OS"

# Check if Python is installed
echo ""
echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed!"
        echo ""
        echo "📥 Please install Python 3.7 or later:"
        if [ "$OS" = "Darwin" ]; then
            echo "   • Visit: https://www.python.org/downloads/"
            echo "   • Or run: brew install python"
        elif [ "$OS" = "Linux" ]; then
            echo "   • Ubuntu/Debian: sudo apt-get install python3 python3-pip"
            echo "   • Or visit: https://www.python.org/downloads/"
        else
            echo "   • Visit: https://www.python.org/downloads/"
        fi
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✅ Python version: $PYTHON_VERSION"

# Check if pip is available
echo ""
echo "📦 Checking pip installation..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "⚠️  pip not found via python -m pip, trying alternative methods..."
    
    # Try pip3 directly
    if command -v pip3 &> /dev/null; then
        echo "✅ Found pip3 command"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        echo "✅ Found pip command"
        PIP_CMD="pip"
    else
        echo "❌ pip is not available!"
        echo ""
        echo "📥 Please install pip:"
        if [ "$OS" = "Darwin" ]; then
            echo "   • Run: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && $PYTHON_CMD get-pip.py"
            echo "   • Or install via Homebrew: brew install python"
        elif [ "$OS" = "Linux" ]; then
            echo "   • Ubuntu/Debian: sudo apt-get install python3-pip"
        else
            echo "   • Visit: https://pip.pypa.io/en/stable/installation/"
        fi
        exit 1
    fi
else
    echo "✅ pip is available via python -m pip"
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Install/upgrade dependencies
echo ""
echo "📦 Installing/upgrading dependencies..."
if [ -f "requirements.txt" ]; then
    # Try multiple installation methods for maximum compatibility
    if $PIP_CMD install --upgrade -r requirements.txt --user --quiet 2>/dev/null; then
        echo "✅ Dependencies installed/upgraded successfully"
    elif $PIP_CMD install -r requirements.txt --user --quiet 2>/dev/null; then
        echo "✅ Dependencies installed successfully"
    elif $PIP_CMD install --upgrade -r requirements.txt --quiet 2>/dev/null; then
        echo "✅ Dependencies installed/upgraded successfully"
    elif $PIP_CMD install -r requirements.txt --quiet 2>/dev/null; then
        echo "✅ Dependencies installed successfully"
    else
        echo "⚠️  Some dependency installation issues, but continuing..."
        echo "💡 If you encounter issues, try: $PIP_CMD install -r requirements.txt --user"
    fi
else
    echo "⚠️  requirements.txt not found, installing basic dependencies..."
    $PIP_CMD install --upgrade selenium webdriver-manager --user --quiet 2>/dev/null || true
fi

# Check Chrome browser
echo ""
echo "🌐 Checking Chrome browser..."
check_chrome

# Setup ChromeDriver (handled automatically)
echo ""
echo "🔧 ChromeDriver setup..."
echo "✅ ChromeDriver will be handled automatically - no manual setup needed!"

# Final verification
echo ""
echo "🧪 Running final verification..."
if $PYTHON_CMD -c "
import selenium
import webdriver_manager
print('✅ All dependencies verified successfully')
" 2>/dev/null; then
    echo "✅ All systems ready!"
else
    echo "⚠️  Verification failed, but continuing..."
    echo "💡 Dependencies might still work. Try running the script."
fi

echo ""
echo "🚀 Starting QuickBuy Pro..."
echo "=========================================="
echo ""

# Run the automation script
exec $PYTHON_CMD automation.py
