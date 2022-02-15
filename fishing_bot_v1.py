from numpy import true_divide
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyautogui
import time
import sys

count = 0
keyboard_controller = Controller()

def on_press(key):
    pass
    # try:
    #     print('alphanumeric key {0} pressed'.format(key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(key))

def on_release(key):
    global count
    #print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
    elif key.char == 'p':
        count += 1
        save_screenshot('screenshot', count)

def save_screenshot(name, index):
    screenshot = pyautogui.screenshot(region=(0,0, 1920, 1080))
    name = './{0}_{1}.png'.format(name, index)
    screenshot.save(name)
    print('Save screenshot '+ name)


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
time.sleep(2)
while True:
    keyboard_controller.press('5')
    time.sleep(2.3)
    keyboard_controller.release('5')
    time.sleep(1)
    start_time = time.clock_gettime(0)
    while pyautogui.locateOnScreen('fishing_hook.jpg', grayscale=True, region=(925, 275, 60, 60), confidence=0.85) == None:
        time_passed = time.clock_gettime(0) - start_time
        sys.stdout.write('waiting for hook {0}s \r'.format(time_passed))
        sys.stdout.flush()
    print("fish on")
    keyboard_controller.press('5')
    time.sleep(2)
    fish_on = True
    is_reel_pressed = True
    while fish_on:
        should_reel = pyautogui.locateOnScreen('r2.jpg', region=(1680, 980, 80, 50), confidence=0.90) != None
        if should_reel and not is_reel_pressed:
            keyboard_controller.press('5')
            is_reel_pressed = True
            print("Reel fish")
        elif not should_reel and is_reel_pressed:
            keyboard_controller.release('5')
            is_reel_pressed = False
            print("Pause reel")

        if not should_reel:
            fish_caught = pyautogui.locateOnScreen('fish_complete.jpg', region=(600, 300, 620, 500), confidence=0.90) != None
            if fish_caught:
                fish_on = False
                print("Fishing completed")
        time.sleep(0.2)
    time.sleep(5)