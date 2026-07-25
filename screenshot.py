import pyautogui
import time
import pyscreeze

# pyautogui.typewrite("Hello! World!", interval=0.1)

# #hot keys
# pyautogui.hotkey('ctrl','c') #Ctrl + C
# pyautogui.hotkey('ctrl','v') #Ctrl + v

# #press
# pyautogui.press('esc')

# #holding down keys
# pyautogui.keyDown('shift')
# pyautogui.typewrite("Uppercase")
# pyautogui.keyUp('shift')

#screenshot
screenshot = pyautogui.screenshot()
screenshot.save("final.png")
pic= pyautogui.screenshot()

pic.save('screenshot.png')
