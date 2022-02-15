import numpy as np
from numpy import fabs, true_divide
from pynput import keyboard
from pynput.keyboard import Key, Controller
from mss import mss
import pyautogui
import time
import sys
import cv2

count = 0
keyboard_controller = Controller()
sct = mss()

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
    name = './{0}_{1}.png'.format(name, index)
    sct.shot(mon=1, output=name)
    print('Save screenshot '+ name)


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

fish_detection_title = 'Fish Detection'
hooking_rect = { "top": 260, "left": 925, "width": 70, "height": 80 }
reel_rect = { "top": 980, "left": 1680, "width": 50, "height": 30 }
complete_rect = { "top": 250, "left": 100, "width": 1720, "height": 700 }

hook_template = cv2.imread('./fishing_hook.jpg', cv2.IMREAD_GRAYSCALE)
reel_template = cv2.imread('./r2.jpg', cv2.IMREAD_GRAYSCALE)
complete_template = cv2.imread('./fish_complete.jpg', cv2.IMREAD_GRAYSCALE)
complete_mask_template = cv2.imread('./fish_complete_mask.jpg', cv2.IMREAD_GRAYSCALE)
quicktime_template = cv2.imread('./r3.jpg', cv2.IMREAD_GRAYSCALE)
r3_direction_templates = [
    cv2.imread('./r3_left_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_right_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_up_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_down_template.jpg', cv2.IMREAD_GRAYSCALE),
]
r3_direction_mask_templates = [
    cv2.imread('./r3_left_mask_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_right_mask_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_up_mask_template.jpg', cv2.IMREAD_GRAYSCALE),
    cv2.imread('./r3_down_mask_template.jpg', cv2.IMREAD_GRAYSCALE),
]            
r3_direction_keys = [ 'j', 'l', 'i', 'k']

fullscreen_grab = cv2.imread('./screenshot_r3_up.png', cv2.IMREAD_GRAYSCALE)
screengrab = fullscreen_grab[complete_rect['top']:complete_rect['top']+complete_rect['height'], complete_rect['left']:complete_rect['left']+complete_rect['width']]

# print(time.clock_gettime(0))
# threshold = 0.9
# screenshot = screengrab.copy()
# result = cv2.matchTemplate(screengrab, quicktime_template, cv2.TM_CCOEFF_NORMED)
# locations = np.where(result >= threshold    )
# locations = list(zip(*locations[::-1]))
# print(time.clock_gettime(0))
# if locations:
#     r3_size = 45
#     bottom_right = (locations[0][0] + quicktime_template.shape[1], locations[0][1] + quicktime_template.shape[0])
#     subrect = { "left" : locations[0][0] - r3_size, "right" : bottom_right[0] + r3_size, "top": locations[0][1] - r3_size, "bottom": bottom_right[1] + r3_size }
#     r3_area = screengrab[subrect['top']:subrect['bottom'], subrect['left']:subrect['right']]
#     cv2.imshow('Sub area', r3_area)
    
#     for (template, mask, r3_direction_key) in zip(r3_direction_templates, r3_direction_mask_templates, r3_direction_keys):
#         result = cv2.matchTemplate(r3_area, template, cv2.TM_CCOEFF_NORMED, mask)
#         sub_locations = np.where(result >= 0.9)
#         sub_locations = list(zip(*sub_locations[::-1]))
#         if sub_locations:
#             print('Found hit. Pressing key: '+ r3_direction_key)
#             break

#     cv2.rectangle(screenshot, (subrect['left'], subrect['top']), (subrect['right'], subrect['bottom']), (0, 255, 0), 2)
#     cv2.rectangle(screenshot, locations[0], bottom_right, (0, 255, 0), 2)
   
# cv2.imshow('Test', screenshot)
# cv2.moveWindow('Test', 1920, 0)
# cv2.waitKey(0)
# exit()


time.sleep(3)

while True:
    print("Start Fishing")
    keyboard_controller.press('5')
    time.sleep(2.3)
    keyboard_controller.release('5')
    time.sleep(1)
    waiting_for_hook = True
    print("Waiting for fish")
    while(waiting_for_hook):
        screenshot = np.array(sct.grab(hooking_rect))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, hook_template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.87)
        locations = list(zip(*locations[::-1]))
        if locations:
            waiting_for_hook = False
            bottom_right = (locations[0][0] + hook_template.shape[1], locations[0][1] + hook_template.shape[0])
    #        cv2.rectangle(screenshot, locations[0], bottom_right, (0, 255, 0), 2)
    #    cv2.imshow(fish_detection_title, screenshot) 
    #    cv2.moveWindow(fish_detection_title, 1920, 0)
        
    #    if cv2.waitKey(1) == ord('q'):
    #        exit()

    print("Fish on")
    fish_on = True
    is_reel_pressed = True

    keyboard_controller.press('5')
    time.sleep(3)

    while fish_on:
        should_reel = False
        screenshot = np.array(sct.grab(reel_rect))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)    
        result = cv2.matchTemplate(gray, reel_template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            should_reel = True

        if should_reel and not is_reel_pressed:
            keyboard_controller.press('5')
            is_reel_pressed = True
            print("Reel fish")
        elif not should_reel and is_reel_pressed:
            keyboard_controller.release('5')
            is_reel_pressed = False
            print("Pause reel")

        if not should_reel:
            screenshot = np.array(sct.grab(complete_rect))
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)    
            result = cv2.matchTemplate(gray, complete_template, cv2.TM_CCOEFF_NORMED, complete_mask_template)
            # cv2.imshow(fish_detection_title, gray) 
            # cv2.moveWindow(fish_detection_title, 1920, 0)
        
            # if cv2.waitKey(1) == ord('q'):5
            #     exit()            
            locations = np.where(result >= 0.9)
            locations = list(zip(*locations[::-1]))
            if locations:
                fish_on = False
                print("Fishing completed")
            else:
                result = cv2.matchTemplate(gray, quicktime_template, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= 0.9)
                locations = list(zip(*locations[::-1]))

                if locations:
                    r3_size = 60
                    bottom_right = (locations[0][0] + quicktime_template.shape[1], locations[0][1] + quicktime_template.shape[0])
                    subrect = { "left" : locations[0][0] - r3_size, "right" : bottom_right[0] + r3_size, "top": locations[0][1] - r3_size, "bottom": bottom_right[1] + r3_size }
                    r3_area = gray[subrect['top']:subrect['bottom'], subrect['left']:subrect['right']]

                    for (template, mask, r3_direction_key) in zip(r3_direction_templates, r3_direction_mask_templates, r3_direction_keys):
                        result = cv2.matchTemplate(r3_area, template, cv2.TM_CCOEFF_NORMED, mask)
                        sub_locations = np.where(result >= 0.85)
                        sub_locations = list(zip(*sub_locations[::-1]))
                        if sub_locations:
                            print('Pressing key: '+ r3_direction_key)
                            keyboard_controller.press(r3_direction_key)
                            time.sleep(0.05)
                            keyboard_controller.release(r3_direction_key)
                            break

    time.sleep(5)