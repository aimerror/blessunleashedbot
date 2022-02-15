import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import sys

sensitivity = sys.argv[1] if len(sys.argv) > 1 else 'default'

keyboard_controller = Controller()

time.sleep(1.0)
keyboard_controller.press('o')
time.sleep(0.1)
keyboard_controller.release('o')
time.sleep(1.0)
keyboard_controller.press('f')
time.sleep(0.1)
keyboard_controller.release('f')
time.sleep(1.0)
keyboard_controller.press('g')
time.sleep(0.1)
keyboard_controller.release('g')
time.sleep(1.0)
keyboard_controller.press('g')
time.sleep(0.1)
keyboard_controller.release('g')
time.sleep(1.0)

for i in range(5):
    keyboard_controller.press(Key.down)
    time.sleep(0.1)
    keyboard_controller.release(Key.down)
    time.sleep(0.1)

if sensitivity == 'slow':
    keyboard_controller.press(Key.left)
    time.sleep(1.5)
    keyboard_controller.release(Key.left)
else:
    for i in range(24):
        keyboard_controller.press(Key.right)
        time.sleep(0.1)
        keyboard_controller.release(Key.right)
        time.sleep(0.05)

time.sleep(0.5)

keyboard_controller.press('t')
time.sleep(0.1)
keyboard_controller.release('t')
time.sleep(1.0)
keyboard_controller.press('t')
time.sleep(0.1)
keyboard_controller.release('t')
time.sleep(2.0)