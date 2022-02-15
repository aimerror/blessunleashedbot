import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import sys

TOTAL_FISH = int(sys.argv[1])
SALVAGE_SELECTION = int(sys.argv[2])

keyboard_controller = Controller()
time.sleep(2.0)
keyboard_controller.press('f')
time.sleep(0.1)
keyboard_controller.release('f')
time.sleep(1.0)
keyboard_controller.press('g')
time.sleep(0.1)
keyboard_controller.release('g')
time.sleep(2.0)

steps = int(TOTAL_FISH / SALVAGE_SELECTION)

for current_step in range(steps):
    for slot in range(SALVAGE_SELECTION):
        keyboard_controller.press('g')
        time.sleep(0.1)
        keyboard_controller.release('g')
        time.sleep(0.2)
        keyboard_controller.press(Key.down)
        time.sleep(0.1)
        keyboard_controller.release(Key.down)
        time.sleep(0.2)
    keyboard_controller.press('g')
    time.sleep(1)
    keyboard_controller.release('g')
    time.sleep(0.5)
    keyboard_controller.press('g')
    time.sleep(0.1)
    keyboard_controller.release('g')
    time.sleep(2.0)
keyboard_controller.press('t')
time.sleep(0.1)
keyboard_controller.release('t')
time.sleep(0.5)
keyboard_controller.press('t')
time.sleep(0.1)
keyboard_controller.release('t')
time.sleep(1.0)