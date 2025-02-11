#!usr/bin/usr python3

import pynput.keyboard

def processKeyPress(key):
    print(key)

keyboardListener = pynput.keyboard.Listener(on_press=processKeyPress)

with keyboardListener:
    keyboardListener.join()

