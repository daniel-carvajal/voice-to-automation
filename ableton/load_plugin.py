import pyautogui
import time
import json

expressions = None

with open('ableton/expressions.json', 'r') as jsonfile:
    expressions = json.load(jsonfile)

def load_plugin(plugin_name):
    # Trim the plugin name
    plugin_cleaned = plugin_name.strip()

    # Simulate 'cmd + f' to focus on the search box

    # Press and hold the 'command' key
    pyautogui.keyDown('command')
    # Wait a short moment for the key to be recognized as held down
    time.sleep(0.1)
    # Press the 'f' key while 'command' is held down
    pyautogui.press('f')
    time.sleep(0.1)
    pyautogui.keyUp('command')

    time.sleep(0.5)  # Wait for the search box to focus

    # # Type the search query for the plugin
    pyautogui.write(plugin_cleaned)
    time.sleep(0.5)

    # # Press the down arrow key to select the first result
    pyautogui.press('down')
    # # Press 'return' to load the plugin
    pyautogui.press('enter')
    time.sleep(0.4)
    pyautogui.press('escape')

    hideSideMenu()
    time.sleep(0.4)
    # hidePlugins()

def hideSideMenu():
    pyautogui.keyDown('command')
    time.sleep(0.1)
    pyautogui.keyDown('option')
    time.sleep(0.1)
    pyautogui.press('b')
    pyautogui.keyUp('command')
    pyautogui.keyUp('option')

def hidePlugins():
    pyautogui.keyDown('command')
    time.sleep(0.1)
    pyautogui.keyDown('option')
    time.sleep(0.1)
    pyautogui.press('p')
    pyautogui.keyUp('command')
    pyautogui.keyUp('option')

def load_from_library(rhino_intention):
    try:
        load_plugin(expressions[rhino_intention])
    except Exception as e: 
        print(e)