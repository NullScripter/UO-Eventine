__author__ = "NullScript"
__version__ = "1.0"

import os, wmi
import pyautogui
import time

## Personal Settings ##
RE_PATH = r"D:\Games\UO Eventine\Eventine Setup\ClassicUO\Data\Plugins\RazorEnhanced-0.8.2.115\RazorEnhanced.exe"
SHOW_RE_LAUNCHER = False # Set to true if not skipping RE Launch window (RE > General > Show Launch Window)
RESTART_CLIENT = 12000 # 20 minutes 

'''
NOTES:
    * This script restarts RE/CUO every 20 minutes:
        1) It closes any windows process named "ClassicUO" (if open)
        2) It launches RE
        3) It clicks the "Launch" button on RE
        4) It clicks "Login" button on CUO
    * The launch and login button images should be in the same folder as this script.

RUNNING:
    * You need python installed.
    * You need pyautogui library (`pip install pyautogui`)
    * Open Windows Power Shell as an admin, navigate to this script folder and run: `python .\auto_restart.py`
'''


## Script ##
def RestartRazorEnhanced():
    f = wmi.WMI()
    for process in f.Win32_Process():
        if 'ClassicUO' not in process.Name: continue
        print(f"Killing {process.ProcessId:<10} {process.Name}") 
        process.Terminate()
    print(f"Starting RazorEnhanced:") 
    os.startfile(RE_PATH)


def ClickToLogin():
    while True:
        print(f"Locating Login Button") 
        box = None

        try: box = pyautogui.locateOnScreen('login_button_off.png')
        except: pass
        if box is not None: break

        try: box = pyautogui.locateOnScreen('login_button_on.png')
        except: pass
        if box is not None: break

        time.sleep(1)

    print(f"Login Location {box}") 
    pyautogui.click(box.left+box.width//2, box.top+box.height//2)
        

def ClickToLaunch():
    while True:
        print(f"Locating Launch CUO Button") 
        try:
            box = pyautogui.locateOnScreen('launch_cuo.png')
            print(f"Launch CUO {box}") 
            pyautogui.click(box.left, box.top)
            break
        except Exception as e:
            time.sleep(1)


def AutoLoop():
    while True:
        RestartRazorEnhanced()
        if SHOW_RE_LAUNCHER: ClickToLaunch()
        ClickToLogin()
        time.sleep(RESTART_CLIENT)


AutoLoop()