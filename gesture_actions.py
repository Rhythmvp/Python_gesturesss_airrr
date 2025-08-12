import pyautogui
import os
import subprocess

def perform_action(gesture_name):
    if gesture_name == "PINCH":
        pyautogui.click()
    elif gesture_name == "OPEN_PALM":
        subprocess.Popen("explorer")
    elif gesture_name == "FIST":
        pyautogui.hotkey('win', 'd')
    elif gesture_name == "VICTORY":
        pyautogui.hotkey('ctrl', 'tab')
    elif gesture_name == "THUMB_UP":
        pyautogui.press("volumeup")
    elif gesture_name == "THUMB_DOWN":
        pyautogui.press("volumedown")
