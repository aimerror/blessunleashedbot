import time
from pynput.keyboard import Key, Controller
import pyautogui
import cv2
import numpy as np

keyboard = Controller()
my_time = time.strftime("%H:%M:%S", time.localtime())
print("Start: "+ my_time)
time.sleep(2)
counter = 0
#im1 = pyautogui.screenshot(region=(0,0, 1920, 1080))
#im1.save("./screen.png")
while 1:
    while pyautogui.locateOnScreen('./character_select.jpg') == None:
        time.sleep(1)
    print("character selected")
    time.sleep(0.4)
    keyboard.press('g')
    time.sleep(0.1)
    keyboard.release('g')
    time.sleep(5)
    while pyautogui.locateOnScreen('./welcome_screen.jpg') == None:
        time.sleep(1)
    print("Welcome screen active")
    time.sleep(0.5)
    keyboard.press('t')
    time.sleep(0.1)
    keyboard.release('t')
    print("Closing welcome screen")
    time.sleep(1)

    while pyautogui.locateOnScreen('./mission.jpg', confidence=0.85) != None:
        print("grab item")
        keyboard.press('f')
        time.sleep(2.2)
        keyboard.release('f')
        time.sleep(0.5)

    time.sleep(0.5)
    print("Exit to character select")
    counter = counter + 1
    keyboard.press(Key.f1)
    time.sleep(0.2)
    keyboard.release(Key.f1)
    time.sleep(1)
    keyboard.press('f')
    time.sleep(0.2)
    keyboard.release('f')
    time.sleep(1.0)
    keyboard.press(Key.up)
    time.sleep(0.1)
    keyboard.release(Key.up)
    time.sleep(0.5)
    if counter < 20:
        keyboard.press(Key.up)
        time.sleep(0.1)
        keyboard.release(Key.up)
        time.sleep(0.5)
    else:
        counter = 0
    keyboard.press('g')
    time.sleep(0.1)
    keyboard.release('g')
    time.sleep(1.0)
    keyboard.press('g')
    time.sleep(0.1)
    keyboard.release('g')
    time.sleep(1)

# im1 = pyautogui.screenshot(region=(0,0, 1920, 1080))
# im1 = np.array(im1)
# # Convert RGB to BGR 
# im1 = im1[:, :, ::-1].copy()
# cv2.imshow("screenshot", im1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()t