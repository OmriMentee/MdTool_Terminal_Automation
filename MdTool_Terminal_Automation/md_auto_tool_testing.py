import math
import time
import pycandle
import keyboard
import time
import sys
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def approve_calib():
    keyboard.write(" Y", delay=0.1)
    keyboard.press("enter")

def auto_calibraion(id):
    keyboard.write(" Y", delay=0.1)
    keyboard.press("enter")
    os.system("mdtool setup calibration " + str(id))


# auto_calibraion(200)
print("hi")
