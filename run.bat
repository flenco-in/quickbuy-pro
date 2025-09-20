@echo off
REM QuickBuy Pro - One-Click Purchase Automation
REM Author: flenco.in
REM Support: https://buymeacoffee.com/atishpaul

echo ==========================================
echo QuickBuy Pro - One-Click Purchase Automation
echo ==========================================
echo Author: flenco.in
echo Support: https://buymeacoffee.com/atishpaul
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7 or later.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo.
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ Dependencies installed successfully
    ) else (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo ⚠️  requirements.txt not found, skipping dependency installation
)

REM Check if ChromeDriver exists locally
if exist "chromedriver.exe" (
    echo ✅ Local ChromeDriver found: chromedriver.exe
) else (
    echo ⚠️  Local ChromeDriver not found, will use system ChromeDriver or webdriver-manager
)

echo.
echo 🚀 Starting QuickBuy Pro...
echo.

REM Run the automation script
python flipkart_automation.py

pause
