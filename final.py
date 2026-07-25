import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

print("Open the safari browser")
time.sleep(2)

pyautogui.hotkey('command','space',interval=0.1)
time.sleep(5)
pyautogui.write('safari')
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

pyautogui.hotkey('command','t',interval=1)
time.sleep(1)
pyautogui.write('https://www.data.gov.in')
time.sleep(1)
pyautogui.press('enter')
time.sleep(5)

# Assume the data is already displayed in Safari

# Select all and copy
pyautogui.hotkey('command', 'a')
time.sleep(1)
pyautogui.hotkey('command', 'c')
time.sleep(2)

# Open Excel
pyautogui.hotkey('command', 'space')
time.sleep(1)
pyautogui.write("Microsoft Excel")
pyautogui.press("enter")
time.sleep(5)

# Create a new workbook
pyautogui.hotkey('command', 'n')
time.sleep(2)

# Paste the copied data
pyautogui.hotkey('command', 'v')
time.sleep(2)

# Save the workbook
pyautogui.hotkey('command', 'shift', 's')   # Save As
time.sleep(2)

pyautogui.write("DataGovData")
time.sleep(1)

pyautogui.press("enter")
time.sleep(2)

# Confirm overwrite if prompted
pyautogui.press("enter")
