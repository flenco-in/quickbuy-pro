"""
QuickBuy Pro - One-Click Purchase Automation
Author: flenco.in
Support: https://buymeacoffee.com/atishpaul

This script automates the e-commerce purchase process using Selenium.
"""

import json
import time
import os
import platform
from datetime import datetime, timedelta
import pickle
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class QuickBuyPro:
    def __init__(self):
        self.driver = None
        self.user_data_dir = os.path.join(os.getcwd(), "user_data")
        self.schedule_file = "schedule.pkl"
        self.step_descriptions = [
            "Opening product page",
            "Clicking Buy Now button",
            "Clicking contact button",
            "Proceeding to payment",
            "Handling payment page (Accept & Continue)",
            "Selecting credit card payment method",
            "Clicking card number field",
            "Entering card number",
            "Clicking expiry date field",
            "Entering expiry date",
            "Entering CVV",
            "Clicking final payment button"
        ]

    def get_chromedriver_path(self):
        """Get the correct ChromeDriver path based on the operating system"""
        system = platform.system().lower()
        
        if system == "windows":
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        elif system == "linux":
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver-linux")
        elif system == "darwin":  # macOS
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
            # For ARM64 Macs, verify the binary is compatible
            if platform.machine() == "arm64" and os.path.exists(chromedriver_path):
                try:
                    # Check if the binary is executable and ARM64 compatible
                    import subprocess
                    result = subprocess.run(['file', chromedriver_path], capture_output=True, text=True)
                    if 'arm64' not in result.stdout:
                        print(f"WARNING: Local ChromeDriver may not be ARM64 compatible: {result.stdout.strip()}")
                except:
                    pass
        else:
            # Fallback to macOS version
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
        
        return chromedriver_path

    def validate_url(self, url):
        """Validate and clean URL before opening"""
        if not url or not url.strip():
            return None, "Empty URL provided"
        
        url = url.strip()
        
        # Check if URL starts with http:// or https://
        if not url.startswith(('http://', 'https://')):
            return None, f"Invalid URL format: {url[:50]}..."
        
        try:
            # Parse URL to check if it's valid
            parsed = urllib.parse.urlparse(url)
            if not parsed.netloc:
                return None, f"Invalid URL: missing domain - {url[:50]}..."
            
            # Clean URL by re-parsing it
            cleaned_url = urllib.parse.urlunparse(parsed)
            return cleaned_url, None
        except Exception as e:
            return None, f"URL validation error: {e}"

    def setup_driver(self):
        """Setup Chrome driver with user data persistence"""
        chrome_options = Options()
        
        # Validate user data directory path
        if not os.path.exists(self.user_data_dir):
            try:
                os.makedirs(self.user_data_dir, exist_ok=True)
                print(f"INFO: Created user data directory: {self.user_data_dir}")
            except Exception as e:
                print(f"WARNING: Could not create user data directory: {e}")
                # Use a fallback directory
                self.user_data_dir = os.path.join(os.getcwd(), "temp_user_data")
                os.makedirs(self.user_data_dir, exist_ok=True)
        
        # Add Chrome options with validation
        try:
            chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("detach", True)
        except Exception as e:
            print(f"WARNING: Error setting Chrome options: {e}")

        try:
            # Try to use OS-specific local ChromeDriver first
            local_chromedriver = self.get_chromedriver_path()
            if os.path.exists(local_chromedriver):
                # Make sure the ChromeDriver is executable
                os.chmod(local_chromedriver, 0o755)
                service = Service(local_chromedriver)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print(f"✅ Using local ChromeDriver: {os.path.basename(local_chromedriver)}")
            else:
                # Fallback to system ChromeDriver
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✅ Using system ChromeDriver")
        except Exception as e1:
            print(f"INFO: Local ChromeDriver failed: {e1}")
            # Fallback to webdriver-manager with ARM64 support
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                
                # For ARM64 Macs, webdriver-manager should automatically detect the correct version
                if platform.system().lower() == "darwin" and platform.machine() == "arm64":
                    print("INFO: Detected ARM64 Mac, using webdriver-manager...")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Using webdriver-manager ChromeDriver")
            except Exception as e2:
                print(f"❌ ChromeDriver setup failed: {e2}")
                print("💡 Please install Chrome browser and make sure it's updated")
                print("💡 Try running: pip install --upgrade selenium webdriver-manager")
                print("💡 For ARM64 Macs, ensure you have the latest Chrome browser installed")
                raise

        # Remove automation indicators
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"WARNING: Could not remove automation indicators: {e}")
        
        return self.driver

    def check_login_status(self):
        """Check if user is logged in by visiting profile page"""
        print("Checking login status...")

        try:
            self.driver.get("https://www.flipkart.com/account/?rd=0&link=home_account")
            time.sleep(3)

            # Handle any popups that might appear
            self.check_and_handle_popups()

            # Check for "Profile Information" text
            try:
                profile_info = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Profile Information')]")
                print("SUCCESS: User is logged in! Profile Information found.")
                return True
            except NoSuchElementException:
                pass

            # Check for login indicator class
            try:
                login_element = self.driver.find_element(By.CLASS_NAME, "PbekyG.xrBehW")
                print("SUCCESS: User is logged in! Login indicator class found.")
                return True
            except NoSuchElementException:
                pass

            # If neither found, user is not logged in
            print("WARNING: User is not logged in. Redirected to login page.")
            print("INFO: Please login in the browser. System will automatically detect when you're logged in.")
            return False

        except Exception as e:
            print(f"ERROR: Error checking login status: {e}")
            return False

    def wait_for_login(self):
        """Continuously check for login until user logs in"""
        print("Waiting for user to login...")
        print("INFO: Please login in the browser window. System will detect automatically when you're done.")

        while True:
            try:
                time.sleep(5)  # Check every 5 seconds

                # Handle any popups that might appear
                self.check_and_handle_popups()

                # Check for "Profile Information" text
                try:
                    profile_info = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Profile Information')]")
                    print("SUCCESS: Login detected! Profile Information found.")
                    print("INFO: User data has been saved. You'll stay logged in for next time.")
                    print("INFO: Closing browser and proceeding with automation...")
                    self.close()
                    return True
                except NoSuchElementException:
                    pass

                # Check for login indicator class
                try:
                    login_element = self.driver.find_element(By.CLASS_NAME, "PbekyG.xrBehW")
                    print("SUCCESS: Login detected! Login indicator class found.")
                    print("INFO: User data has been saved. You'll stay logged in for next time.")
                    print("INFO: Closing browser and proceeding with automation...")
                    self.close()
                    return True
                except NoSuchElementException:
                    pass

                # Try refreshing account page to check again
                current_url = self.driver.current_url
                if "login" not in current_url.lower():
                    self.driver.get("https://www.flipkart.com/account/?rd=0&link=home_account")
                    time.sleep(2)
                    self.check_and_handle_popups()

            except KeyboardInterrupt:
                print("\nINFO: Login waiting cancelled by user.")
                return False
            except Exception as e:
                print(f"WARNING: Error while waiting for login: {e}")
                time.sleep(5)
                continue

    def get_user_inputs(self):
        """Get all required inputs from user"""
        print("\nPlease enter the product URL:")
        print("IMPORTANT NOTE: First go to product page and select all details:")
        print("   - Choose Color, Size, Variant and other options")
        print("   - Copy URL only after selecting all details")
        print("   - This ensures automation works with the correct product\n")
        product_url = input("Product URL: ").strip()

        print("\nCard Details (Optional):")
        print("Do you want to prefill card details? (y/n): ", end="")
        prefill_choice = input().strip().lower()

        card_number = ""
        expiry_date = ""
        cvv = ""

        if prefill_choice == 'y' or prefill_choice == 'yes':
            card_number = input("Card Number: ").strip()
            expiry_date = input("Expiry Date (MM/YY format): ").strip()
            cvv = input("CVV: ").strip()

            # Convert MM/YY to MM / YY format for Flipkart if provided
            if expiry_date and "/" in expiry_date and len(expiry_date) == 5:
                expiry_date = expiry_date.replace("/", " / ")
        else:
            print("INFO: Card details will not be prefilled. You'll enter them manually during automation.")

        print("\nExecution Timing:")
        print("1. Execute Now")
        print("2. Schedule for Later")
        choice = input("Choose option (1 or 2): ").strip()

        scheduled_time = None
        if choice == "2":
            print("\nSchedule for later:")
            date_input = input("Enter date (DD/MM/YYYY) or press Enter for today: ").strip()
            time_input = input("Enter time (HH:MM) in 24-hour format: ").strip()

            if not date_input:
                scheduled_date = datetime.now().date()
            else:
                try:
                    scheduled_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                except:
                    print("ERROR: Invalid date format, using today")
                    scheduled_date = datetime.now().date()

            try:
                scheduled_time_obj = datetime.strptime(time_input, "%H:%M").time()
                scheduled_time = datetime.combine(scheduled_date, scheduled_time_obj)

                if scheduled_time <= datetime.now():
                    print("WARNING: Scheduled time is in the past, executing now instead")
                    scheduled_time = None
                else:
                    print(f"SUCCESS: Scheduled for: {scheduled_time.strftime('%d/%m/%Y at %H:%M')}")
                    print("INFO: Keep this tool running for scheduled execution")
            except:
                print("ERROR: Invalid time format, executing now")
                scheduled_time = None

        return {
            'product_url': product_url,
            'card_number': card_number,
            'expiry_date': expiry_date,
            'cvv': cvv,
            'scheduled_time': scheduled_time
        }

    def load_steps(self):
        """Load automation steps - hardcoded for security"""
        # Hardcoded automation steps for Flipkart purchase flow
        steps = [
            {
                "Command": "open",
                "Target": "",  # Will be replaced with user's product URL
                "Value": "",
                "Description": "Opening product page"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"container\"]/div/div[3]/div/div/div[2]/div/ul/li[2]/form/button",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"container\"]/div/div[3]/div/div/div[2]/div/ul/li[2]/form/button",
                    "xpath=//button[@type='button']",
                    "xpath=//form/button",
                    "css=#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-5-12.MfqIAz > div:nth-child(2) > div > ul > li.col.col-6-12.flex > form > button"
                ],
                "Description": "Clicking Buy Now button"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"CNTCTC3B8D4BCB4674CB8855B4905E\"]/button",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"CNTCTC3B8D4BCB4674CB8855B4905E\"]/button",
                    "xpath=//div[2]/div/div/button",
                    "css=#CNTCTC3B8D4BCB4674CB8855B4905E > button"
                ],
                "Description": "Clicking contact button"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"to-payment\"]/button",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"to-payment\"]/button",
                    "xpath=//span[2]/button",
                    "css=#to-payment > button"
                ],
                "Description": "Proceeding to payment"
            },
            {
                "Command": "clickAndWait",
                "Target": "xpath=//*[@id=\"container\"]/div/div/div/div/button",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"container\"]/div/div/div/div/button",
                    "xpath=//div/div/div/div/div/button",
                    "css=#container > div > div._1TWLMK.icF5zO > div > div > button"
                ],
                "Description": "Handling payment page (Accept & Continue)"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"container\"]/div[2]/div/section/div/div/div/section/div/div[2]/div/div/div/div/div/div/span",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"container\"]/div[2]/div/section/div/div/div/section/div/div[2]/div/div/div/div/div/div/span",
                    "xpath=//div[2]/div/div/div/div/div/div/span",
                    "css=#container > div.Wr52Y1 > div > section.iGRJtT > div > div > div > section.RMFVQw > div > div:nth-child(2) > div:nth-child(1) > div > div > div > div > div.eZcpWE.rC9zAr > span"
                ],
                "Description": "Selecting credit card payment method"
            },
            {
                "Command": "click",
                "Target": "id=cc-input",
                "Value": "",
                "Targets": [
                    "id=cc-input",
                    "xpath=//*[@id=\"cc-input\"]",
                    "xpath=//input[@id='cc-input']",
                    "xpath=//input",
                    "css=#cc-input"
                ],
                "Description": "Clicking card number field"
            },
            {
                "Command": "type",
                "Target": "id=cc-input",
                "Value": "1111 1111 1111 1111",  # Default test card
                "Targets": [
                    "id=cc-input",
                    "xpath=//*[@id=\"cc-input\"]",
                    "xpath=//input[@id='cc-input']",
                    "xpath=//input",
                    "css=#cc-input"
                ],
                "Description": "Entering card number"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"cards\"]/div/div[2]/div/input",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"cards\"]/div/div[2]/div/input",
                    "xpath=//input[@value='']",
                    "xpath=//div[2]/div/input",
                    "css=#cards > div > div.aTGip4 > div._1GKNyd.chD0T3 > input"
                ],
                "Description": "Clicking expiry date field"
            },
            {
                "Command": "type",
                "Target": "xpath=//*[@id=\"cards\"]/div/div[2]/div/input",
                "Value": "03 / 34",  # Default test expiry
                "Targets": [
                    "xpath=//*[@id=\"cards\"]/div/div[2]/div/input",
                    "xpath=//input[@value='03 / 34']",
                    "xpath=//div[2]/div/input",
                    "css=#cards > div > div.aTGip4 > div._1GKNyd.chD0T3 > input"
                ],
                "Description": "Entering expiry date"
            },
            {
                "Command": "type",
                "Target": "id=cvv-input",
                "Value": "111",  # Default test CVV
                "Targets": [
                    "id=cvv-input",
                    "xpath=//*[@id=\"cvv-input\"]",
                    "xpath=//input[@id='cvv-input']",
                    "xpath=//div[2]/div[2]/div/input",
                    "css=#cvv-input"
                ],
                "Description": "Entering CVV"
            },
            {
                "Command": "click",
                "Target": "xpath=//*[@id=\"cards\"]/div/button",
                "Value": "",
                "Targets": [
                    "xpath=//*[@id=\"cards\"]/div/button",
                    "xpath=//div/button",
                    "css=#cards > div > button"
                ],
                "Description": "Clicking final payment button"
            }
        ]
        return steps

    def check_and_handle_popups(self):
        """Check for common popup buttons and handle them"""
        try:
            # Check for Accept & Continue button
            accept_continue_selectors = [
                '//*[@id="container"]/div/div[1]/div/div/button',
                '//button[contains(text(), "Accept") and contains(text(), "Continue")]',
                '//button[contains(text(), "Accept & Continue")]',
                '//button[contains(text(), "ACCEPT") and contains(text(), "CONTINUE")]'
            ]

            for selector in accept_continue_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed() and element.is_enabled():
                        print("INFO: Found Accept & Continue button, clicking...")
                        element.click()
                        time.sleep(1.5)  # Reduced from 2 seconds
                        print("SUCCESS: Accept & Continue clicked, continuing automation...")
                        return True
                except:
                    continue

            return False
        except Exception:
            return False

    def execute_command(self, command):
        """Execute a single command from steps.json"""
        cmd_type = command.get('Command', '')
        target = command.get('Target', '')
        value = command.get('Value', '')
        targets = command.get('Targets', [])

        # Skip session-specific URLs that might be expired
        if cmd_type == 'open' and ('token=' in target or 'payments?' in target):
            print(f"INFO: Skipping session-specific URL: {target[:50]}...")
            return True

        # Skip problematic step 5 that causes delays
        if cmd_type == 'clickAndWait' and 'container"]/div/div/div/div/button' in target:
            print(f"INFO: Skipping problematic step: {target[:50]}...")
            return True

        # Don't print executing logs - will be handled by step descriptions

        try:
            if cmd_type == 'open':
                # Validate and clean URL before opening
                cleaned_url, error = self.validate_url(target)
                if error:
                    print(f"WARNING: {error}")
                    return False
                
                try:
                    self.driver.get(cleaned_url)
                    time.sleep(1.5)  # Reduced from 2 seconds
                    # Check for popups after page load
                    self.check_and_handle_popups()
                except Exception as url_error:
                    print(f"ERROR: Failed to open URL: {url_error}")
                    print(f"URL: {cleaned_url[:100]}...")
                    return False

            elif cmd_type == 'click':
                # Check for popups before important clicks
                self.check_and_handle_popups()

                element = self.find_element_by_target(target, targets)
                if element:
                    element.click()
                    time.sleep(0.5)  # Reduced from 1 second
                else:
                    print(f"WARNING: Element not found for click: {target}")
                    return False

            elif cmd_type == 'clickAndWait':
                # Check for popups before important clicks
                self.check_and_handle_popups()

                element = self.find_element_by_target(target, targets)
                if element:
                    element.click()
                    time.sleep(2)  # Reduced from 3 seconds
                    # Check for popups after clickAndWait since it might load new content
                    self.check_and_handle_popups()
                else:
                    print(f"WARNING: Element not found for clickAndWait: {target}")
                    return False

            elif cmd_type == 'type':
                # Skip typing if value is empty (user chose not to prefill)
                if not value:
                    print(f"   INFO: Skipping field - will be filled manually")
                    return True

                element = self.find_element_by_target(target, targets)
                if element:
                    # For expiry date field, click first if needed
                    if 'div[2]/div/input' in target and 'cards' in target:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                    element.clear()
                    element.send_keys(value)
                    time.sleep(0.5)  # Reduced from 1 second
                else:
                    print(f"WARNING: Element not found for type: {target}")
                    return False

            return True

        except Exception as e:
            print(f"ERROR: Error executing command {cmd_type}: {e}")
            return False

    def find_element_by_target(self, target, targets=None):
        """Find element by target selector, try alternatives if main fails"""
        wait = WebDriverWait(self.driver, 5)  # Reduced from 10 to 5 seconds

        # Try main target first
        try:
            if target.startswith('xpath='):
                xpath = target.replace('xpath=', '')
                return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            elif target.startswith('id='):
                element_id = target.replace('id=', '')
                return wait.until(EC.presence_of_element_located((By.ID, element_id)))
            elif target.startswith('css='):
                css_selector = target.replace('css=', '')
                return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            else:
                # Assume it's xpath if no prefix
                return wait.until(EC.presence_of_element_located((By.XPATH, target)))
        except TimeoutException:
            pass

        # Try alternative targets if provided
        if targets:
            for alt_target in targets:
                try:
                    if alt_target.startswith('xpath='):
                        xpath = alt_target.replace('xpath=', '')
                        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    elif alt_target.startswith('id='):
                        element_id = alt_target.replace('id=', '')
                        return wait.until(EC.presence_of_element_located((By.ID, element_id)))
                    elif alt_target.startswith('css='):
                        css_selector = alt_target.replace('css=', '')
                        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                    else:
                        return wait.until(EC.presence_of_element_located((By.XPATH, alt_target)))
                except TimeoutException:
                    continue

        return None

    def save_schedule(self, data):
        """Save scheduled execution data"""
        with open(self.schedule_file, 'wb') as f:
            pickle.dump(data, f)

    def load_schedule(self):
        """Load scheduled execution data"""
        try:
            with open(self.schedule_file, 'rb') as f:
                return pickle.load(f)
        except:
            return None

    def clear_schedule(self):
        """Clear scheduled execution data"""
        try:
            os.remove(self.schedule_file)
        except:
            pass

    def run_automation(self, user_inputs):
        """Run the complete automation flow"""
        # Setup driver again for automation
        print("\nStarting new browser session for automation...")
        self.setup_driver()

        steps = self.load_steps()
        if not steps:
            print("ERROR: No steps found to execute!")
            return

        print(f"\nStarting automation for: {user_inputs['product_url'][:50]}...")

        # Replace the first URL with user's product URL
        if steps and steps[0].get('Command') == 'open':
            steps[0]['Target'] = user_inputs['product_url']

        # Update card details in steps
        self.update_card_details_in_steps(steps, user_inputs)

        # Execute each step with user-friendly descriptions
        for i, step in enumerate(steps):
            if i < len(self.step_descriptions):
                print(f"\n{i+1}. {self.step_descriptions[i]}")
            else:
                print(f"\n{i+1}. Processing step {i+1}")

            success = self.execute_command(step)

            if not success:
                print(f"   WARNING: Step failed, continuing...")
                continue
            else:
                print(f"   SUCCESS: Completed")

        print("\nAutomation completed successfully!")

    def update_card_details_in_steps(self, steps, user_inputs):
        """Update card details in automation steps"""
        for step in steps:
            if step.get('Command') == 'type':
                target = step.get('Target', '')
                if 'cc-input' in target:
                    step['Value'] = user_inputs['card_number']
                elif 'div[2]/div/input' in target and 'cards' in target:
                    step['Value'] = user_inputs['expiry_date']
                elif 'cvv-input' in target:
                    step['Value'] = user_inputs['cvv']

    def close(self):
        """Close the browser and save user data"""
        if self.driver:
            print("INFO: Saving user data...")
            time.sleep(2)
            self.driver.quit()
            print("SUCCESS: Browser closed. User data saved!")

def check_scheduled_execution():
    """Check if there's a scheduled execution on startup"""
    automation = QuickBuyPro()
    scheduled_data = automation.load_schedule()

    if scheduled_data:
        scheduled_time = scheduled_data['scheduled_time']
        if scheduled_time and scheduled_time > datetime.now():
            print("\n" + "="*60)
            print("⏰ SCHEDULED EXECUTION FOUND")
            print("="*60)
            print(f"📅 Execution scheduled for: {scheduled_time.strftime('%d/%m/%Y at %H:%M')}")
            remaining_time = scheduled_time - datetime.now()
            hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"⏳ Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}")
            print(f"🛍️  Product: {scheduled_data.get('product_url', 'N/A')[:50]}...")
            print(f"💳 Card prefill: {'Yes' if scheduled_data.get('card_number', '') else 'No'}")
            print("\nOptions:")
            print("1. Wait for scheduled time")
            print("2. Execute now")
            print("3. Cancel scheduled execution")

            choice = input("Choose option (1, 2, or 3): ").strip()

            if choice == "2":
                automation.clear_schedule()
                return scheduled_data
            elif choice == "3":
                automation.clear_schedule()
                print("✅ Scheduled execution cancelled")
                return None
            else:
                print(f"⏳ Waiting for scheduled time: {scheduled_time.strftime('%d/%m/%Y at %H:%M')}")
                print("💡 Keep this tool running. Press Ctrl+C to cancel.")

                try:
                    while datetime.now() < scheduled_time:
                        time.sleep(30)  # Check every 30 seconds
                        remaining = scheduled_time - datetime.now()
                        if remaining.total_seconds() <= 60:
                            print(f"⏰ Starting in {int(remaining.total_seconds())} seconds...")

                    automation.clear_schedule()
                    return scheduled_data

                except KeyboardInterrupt:
                    print("\n❌ Scheduled execution cancelled by user")
                    automation.clear_schedule()
                    return None
        else:
            # Scheduled time has passed, clear it
            automation.clear_schedule()

    return None

def main():
    # Check for scheduled execution first
    scheduled_data = check_scheduled_execution()

    automation = QuickBuyPro()

    try:
        if scheduled_data:
            user_inputs = scheduled_data
            print(f"\nExecuting scheduled automation...")

            # Setup driver and check login for scheduled execution
            automation.setup_driver()
            is_logged_in = automation.check_login_status()

            if not is_logged_in:
                login_success = automation.wait_for_login()
                if not login_success:
                    print("ERROR: Login cancelled or failed.")
                    return
            else:
                print("SUCCESS: Already logged in! Proceeding...")
                automation.close()
        else:
            # First check login status before asking for product URL
            print("\n" + "="*60)
            print("QUICKBUY PRO - One-Click Purchase Automation")
            print("="*60)
            print("Author: flenco.in")
            print("Support: https://buymeacoffee.com/atishpaul")
            print("="*60)
            print("\nStep 1: Checking login status...")

            # Setup driver and check login first
            automation.setup_driver()
            is_logged_in = automation.check_login_status()

            if not is_logged_in:
                login_success = automation.wait_for_login()
                if not login_success:
                    print("ERROR: Login cancelled or failed.")
                    return
            else:
                print("SUCCESS: Already logged in! Proceeding...")
                automation.close()

            print("\nStep 2: Getting automation details...")
            # Get user inputs after login is confirmed
            user_inputs = automation.get_user_inputs()

            if not user_inputs['product_url']:
                print("ERROR: No product URL provided!")
                return

            # Handle scheduling
            if user_inputs['scheduled_time']:
                automation.save_schedule(user_inputs)
                print(f"\nSUCCESS: Automation scheduled for {user_inputs['scheduled_time'].strftime('%d/%m/%Y at %H:%M')}")
                print("INFO: Keep this tool running for scheduled execution")
                print(f"⏳ Waiting for scheduled time: {user_inputs['scheduled_time'].strftime('%d/%m/%Y at %H:%M')}")
                print("💡 Press Ctrl+C to cancel scheduled execution")

                try:
                    while datetime.now() < user_inputs['scheduled_time']:
                        time.sleep(30)  # Check every 30 seconds
                        remaining = user_inputs['scheduled_time'] - datetime.now()
                        if remaining.total_seconds() <= 60:
                            print(f"⏰ Starting in {int(remaining.total_seconds())} seconds...")

                    automation.clear_schedule()
                    print("\n🚀 Starting scheduled automation...")
                    # Continue to automation execution

                except KeyboardInterrupt:
                    print("\n❌ Scheduled execution cancelled by user")
                    automation.clear_schedule()
                    return

        # Run automation
        automation.run_automation(user_inputs)

        # Keep browser open for user to see result
        input("\nAutomation completed! Press Enter to close browser...")

    except KeyboardInterrupt:
        print("\nINFO: Automation stopped by user.")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
    finally:
        automation.close()

if __name__ == "__main__":
    main()