@echo off
REM QuickBuy Pro - One-Click Purchase Automation
REM Author: flenco.in
REM Support: https://buymeacoffee.com/atishpaul

setlocal enabledelayedexpansion

echo ==========================================
echo QuickBuy Pro - One-Click Purchase Automation
echo ==========================================
echo Author: flenco.in
echo Support: https://buymeacoffee.com/atishpaul
echo ==========================================
echo.

REM Detect Windows architecture
echo 🖥️  Operating System: Windows

REM Check if Python is installed
echo.
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo.
    echo 📥 Please install Python 3.7 or later:
    echo    • Visit: https://www.python.org/downloads/
    echo    • Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python found: python
echo ✅ Python version: !PYTHON_VERSION!

REM Check if pip is available
echo.
echo 📦 Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available!
    echo.
    echo 📥 Please install pip:
    echo    • Run: python -m ensurepip --upgrade
    echo    • Or visit: https://pip.pypa.io/en/stable/installation/
    echo.
    pause
    exit /b 1
)

echo ✅ pip is available

REM Check Chrome browser
echo.
echo 🌐 Checking Chrome browser...
set CHROME_FOUND=0
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%PROGRAMFILES%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1

if %CHROME_FOUND%==0 (
    echo ❌ Chrome browser not found!
    echo.
    echo 📥 Please install Google Chrome:
    echo    • Visit: https://www.google.com/chrome/
    echo    • Download and install Chrome
    echo    • Restart this script after installation
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
) else (
    echo ✅ Chrome browser found
)

REM Install/upgrade dependencies
echo.
echo 📦 Installing/upgrading dependencies...
if exist "requirements.txt" (
    echo 📦 Installing from requirements.txt...
    python -m pip install --upgrade -r requirements.txt --user --quiet >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Dependencies installed/upgraded successfully
    ) else (
        python -m pip install -r requirements.txt --user --quiet >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Dependencies installed successfully
        ) else (
            python -m pip install --upgrade -r requirements.txt --quiet >nul 2>&1
            if %errorlevel% equ 0 (
                echo ✅ Dependencies installed/upgraded successfully
            ) else (
                echo ⚠️  Some dependency installation issues, but continuing...
                echo 💡 If you encounter issues, try: python -m pip install -r requirements.txt --user
            )
        )
    )
) else (
    echo ⚠️  requirements.txt not found, installing basic dependencies...
    python -m pip install --upgrade selenium webdriver-manager --user --quiet >nul 2>&1
)

REM Setup ChromeDriver (handled automatically)
echo.
echo 🔧 ChromeDriver setup...
echo ✅ ChromeDriver will be handled automatically - no manual setup needed!

REM Final verification
echo.
echo 🧪 Running final verification...
python -c "import selenium; import webdriver_manager; print('✅ All dependencies verified successfully')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ All systems ready!
) else (
    echo ❌ Verification failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting QuickBuy Pro...
echo ==========================================
echo.

REM Run the automation script
python automation.py

echo.
echo Automation completed. Press any key to exit...
pause >nul
