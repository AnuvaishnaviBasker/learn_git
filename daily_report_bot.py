"""
Daily Status Report Bot
Automates browser data fetching, Excel entry, and reporting via PyAutoGUI
Medium-level automation task
"""

import pyautogui
import time
import subprocess
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import platform
import json
import pyperclip

# Configuration
SCREENSHOT_DELAY = 1  # seconds to wait for UI to settle
APP_LAUNCH_DELAY = 3  # seconds to wait for app to open
REPORT_DIR = os.path.expanduser("~/Desktop/Daily_Reports")

# Ensure report directory exists
os.makedirs(REPORT_DIR, exist_ok=True)

class DailyReportBot:
    def __init__(self):
        self.system = platform.system()
        self.current_date = datetime.now()
        self.current_time_str = self.current_date.strftime("%Y-%m-%d %H:%M:%S")
        self.date_str = self.current_date.strftime("%Y-%m-%d")
        self.fetched_data = None
        self.comment = ""
        
    def wait_and_log(self, message, duration=SCREENSHOT_DELAY):
        """Log message and wait"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        time.sleep(duration)
    
    def take_screenshot(self, filename):
        """Take a screenshot and save it"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"✓ Screenshot saved: {filename}")
            return True
        except Exception as e:
            print(f"✗ Screenshot failed: {e}")
            return False
    
    def fetch_weather_data(self):
        """Fetch weather data from a public API"""
        try:
            self.wait_and_log("Fetching weather data from API...")
            
            # Using wttr.in API (no key required)
            response = requests.get("https://wttr.in/?format=j1", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            current_condition = data['current_condition'][0]
            temp = current_condition['temp_C']
            description = current_condition['weatherDesc'][0]['value']
            
            self.fetched_data = f"Temp: {temp}°C, Condition: {description}"
            
            # Generate comment based on weather
            if temp > 25:
                self.comment = "Good for outdoor activities"
            elif temp > 15:
                self.comment = "Moderate temperature, pleasant day"
            else:
                self.comment = "Cold, bring jacket"
            
            print(f"✓ Weather data fetched: {self.fetched_data}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to fetch weather: {e}")
            # Fallback data
            self.fetched_data = "Weather data unavailable"
            self.comment = "Check website manually"
            return False
    
    def open_chrome_and_verify(self):
        """Open Chrome browser"""
        try:
            self.wait_and_log("Opening Chrome browser...", APP_LAUNCH_DELAY)
            
            if self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Google Chrome", "https://wttr.in"])
            elif self.system == "Windows":
                subprocess.Popen(["chrome", "https://wttr.in"])
            else:  # Linux
                subprocess.Popen(["google-chrome", "https://wttr.in"])
            
            time.sleep(APP_LAUNCH_DELAY)
            pyautogui.click(500, 300)  # Click on the window to focus
            self.wait_and_log("Chrome opened and focused")
            return True
            
        except Exception as e:
            print(f"✗ Failed to open Chrome: {e}")
            return False
    
    def open_spreadsheet(self):
        """Open Numbers (Mac) or Excel"""
        try:
            self.wait_and_log("Opening spreadsheet application...", APP_LAUNCH_DELAY)
            
            if self.system == "Darwin":  # macOS
                # Check if Numbers exists
                result = subprocess.run(
                    ["mdfind", "-name", "Numbers.app"],
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    subprocess.Popen(["open", "-a", "Numbers"])
                else:
                    # Fallback to Excel
                    subprocess.Popen(["open", "-a", "Microsoft Excel"])
            else:
                subprocess.Popen(["excel"])  # Windows
            
            time.sleep(APP_LAUNCH_DELAY)
            self.wait_and_log("Spreadsheet application opened")
            return True
            
        except Exception as e:
            print(f"✗ Failed to open spreadsheet: {e}")
            return False
    
    def create_new_spreadsheet(self):
        """Create a new spreadsheet or open template"""
        try:
            self.wait_and_log("Creating new spreadsheet...")
            
            # Use keyboard shortcut for new document
            pyautogui.hotkey('cmd', 'n') if self.system == "Darwin" else pyautogui.hotkey('ctrl', 'n')
            time.sleep(SCREENSHOT_DELAY)
            
            # In case a dialog appears
            pyautogui.press('enter')
            time.sleep(SCREENSHOT_DELAY)
            
            self.wait_and_log("New spreadsheet created")
            return True
            
        except Exception as e:
            print(f"✗ Failed to create spreadsheet: {e}")
            return False
    
    def enter_report_data(self):
        """Enter data into spreadsheet"""
        try:
            self.wait_and_log("Entering report data into spreadsheet...")
            
            # Click on first cell (A1)
            pyautogui.click(100, 100)
            time.sleep(SCREENSHOT_DELAY)
            
            # Enter headers if needed
            pyautogui.typewrite('Date_Time', interval=0.05)
            pyautogui.press('tab')
            pyautogui.typewrite('Data', interval=0.05)
            pyautogui.press('tab')
            pyautogui.typewrite('Comment', interval=0.05)
            pyautogui.press('enter')
            
            # Move to first data row
            time.sleep(SCREENSHOT_DELAY)
            
            # Enter data
            pyautogui.typewrite(self.current_time_str, interval=0.02)
            pyautogui.press('tab')
            pyautogui.typewrite(self.fetched_data, interval=0.02)
            pyautogui.press('tab')
            pyautogui.typewrite(self.comment, interval=0.02)
            pyautogui.press('enter')
            
            self.wait_and_log("Report data entered successfully")
            return True
            
        except Exception as e:
            print(f"✗ Failed to enter data: {e}")
            return False
    
    def save_spreadsheet(self):
        """Save the spreadsheet with date-stamped filename"""
        try:
            self.wait_and_log("Saving spreadsheet...")
            
            # Use Save As
            pyautogui.hotkey('cmd', 's') if self.system == "Darwin" else pyautogui.hotkey('ctrl', 's')
            time.sleep(SCREENSHOT_DELAY * 2)
            
            # Filename with date
            filename = f"daily_report_{self.date_str}.xlsx"
            filepath = os.path.join(REPORT_DIR, filename)
            
            # Type filename
            pyautogui.typewrite(filename, interval=0.02)
            time.sleep(SCREENSHOT_DELAY)
            
            # Press enter or click save
            pyautogui.press('enter')
            time.sleep(APP_LAUNCH_DELAY)
            
            self.wait_and_log(f"Spreadsheet saved: {filepath}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to save spreadsheet: {e}")
            return False
    
    def capture_final_screenshot(self):
        """Capture final screenshot of the report"""
        try:
            self.wait_and_log("Capturing final screenshot...")
            
            screenshot_filename = os.path.join(
                REPORT_DIR,
                f"daily_report_screenshot_{self.date_str}.png"
            )
            
            self.take_screenshot(screenshot_filename)
            self.wait_and_log(f"Final screenshot saved: {screenshot_filename}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to capture screenshot: {e}")
            return False
    
    def generate_report_summary(self):
        """Generate and save a text summary of the report"""
        try:
            summary_file = os.path.join(
                REPORT_DIR,
                f"daily_report_summary_{self.date_str}.txt"
            )
            
            summary = f"""
DAILY STATUS REPORT SUMMARY
{'='*50}
Generated: {self.current_time_str}
Date: {self.date_str}

FETCHED DATA:
{self.fetched_data}

COMMENT:
{self.comment}

SYSTEM INFO:
Platform: {self.system}
Report Directory: {REPORT_DIR}

FILES CREATED:
- daily_report_{self.date_str}.xlsx
- daily_report_screenshot_{self.date_str}.png
- daily_report_summary_{self.date_str}.txt

{'='*50}
            """
            
            with open(summary_file, 'w') as f:
                f.write(summary)
            
            print(f"\n✓ Report summary saved: {summary_file}")
            print(summary)
            return True
            
        except Exception as e:
            print(f"✗ Failed to generate summary: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("DAILY REPORT BOT - Starting Automation")
        print("="*60)
        print(f"Current Date/Time: {self.current_time_str}")
        print(f"Report Directory: {REPORT_DIR}")
        print("="*60 + "\n")
        
        try:
            # Step 1: Fetch data
            if not self.fetch_weather_data():
                print("⚠ Warning: Could not fetch weather data, continuing with fallback")
            
            # Step 2: Open browser
            if not self.open_chrome_and_verify():
                print("⚠ Warning: Could not open Chrome, continuing...")
            
            self.wait_and_log("Giving browser time to load...", 2)
            
            # Step 3: Open spreadsheet
            if not self.open_spreadsheet():
                print("✗ Critical: Could not open spreadsheet")
                return False
            
            # Step 4: Create new document
            if not self.create_new_spreadsheet():
                print("⚠ Warning: Could not create new spreadsheet, using existing")
            
            # Step 5: Enter data
            if not self.enter_report_data():
                print("✗ Critical: Could not enter data")
                return False
            
            # Step 6: Save spreadsheet
            if not self.save_spreadsheet():
                print("✗ Critical: Could not save spreadsheet")
                return False
            
            # Step 7: Capture screenshot
            if not self.capture_final_screenshot():
                print("⚠ Warning: Could not capture screenshot")
            
            # Step 8: Generate summary
            self.generate_report_summary()
            
            print("\n" + "="*60)
            print("✓ DAILY REPORT BOT - Completed Successfully!")
            print("="*60 + "\n")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠ Bot interrupted by user")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            return False


def main():
    """Entry point"""
    bot = DailyReportBot()
    success = bot.run()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
