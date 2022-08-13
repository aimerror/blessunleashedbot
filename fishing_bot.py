import window_info
import threading
#import screenshot
import cv2 as cv
import numpy as np
import time
import datetime
from mss import mss
from pynput import keyboard
from pynput.keyboard import Key, Controller
import logging
import log_message
import sys
import subprocess
import online_log
import config
import os
import psutil
import signal

LOCATION_SCRIPT = ''
TOTAL_FISH = 200
SALVAGE_SELECTION = 20
TOTAL_RUNTIME = 240
bait_used = 0

def select_location():
    global LOCATION_SCRIPT
    locations = ['downstream', 'lake_ezren']
    print("")
    print("[1] downstream")
    print("[2] lake ezren")
    print("[0] exit")

    option = int(input("Select fishing locations: "))
    if option > 2:
        print("Invalid option location selected")
        select_location()
    elif option == 0:
        exit()
    else:
        LOCATION_SCRIPT = locations[option - 1]
        print("Selected fishing location: {0}".format(LOCATION_SCRIPT))

def select_total_fish():
    global TOTAL_FISH
    global SALVAGE_SELECTION 
    print("")
    option = int(input("How many times to fish before salvaging: "))
    if option == 0:
        print("Enter minimum of 1")
        select_total_fish()
    TOTAL_FISH = option
    SALVAGE_SELECTION = min(TOTAL_FISH, 20)
    print("{0} fishing attemps selected".format(TOTAL_FISH))

def select_runtime():
    global TOTAL_RUNTIME
    print("")
    option = int(input("Run bot for x minutes before autoshutdown: "))
    if option == 0:
        print("Enter minimum of 1 minute or higer")
        select_runtime()
    TOTAL_RUNTIME = option
    print("Bot will shutdown PlayStation and PC after {0} minutes".format(TOTAL_RUNTIME))
    print("")

def kill_all_children():
    print("checking processes")
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        os.kill(child.pid, signal.SIGTERM)

def program_timer(delta):
    countdown = delta
    while countdown > 0:
        logging.info('closing program in {0} {1}'.format(countdown, 'minute' if countdown == 1 else 'minutes'))
        online_log.log('closing program in {0} {1}'.format(countdown, 'minute' if countdown == 1 else 'minutes'), 'a+')
        time.sleep(60)
        countdown -= 1

    time.sleep(1.0)
    kill_all_children()
    subprocess.Popen('python shutdown.py {}'.format('shutdown_script'))
    os._exit(1)

def draw_preview(title, image):
    global window_rect
    # font = cv.FONT_HERSHEY_SIMPLEX
    # org = (5, 15)
    # font_scale = 0.5
    # color = (255, 255, 255)  
    # thickness = 1
    # framerate = 'FPS {}'.format(int(1 / (time() - loop_time)))
    # screen_colored = cv.putText(image, framerate, org, font, font_scale, color, thickness, cv.LINE_AA)    
    cv.imshow(title, image)
    cv.moveWindow(title, window.x + window.width - window.border_size, window.y)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

hook_template = cv.imread('./fish_assets/hook_template.png', cv.IMREAD_GRAYSCALE)
reel_template = cv.imread('./fish_assets/r2.png', cv.IMREAD_GRAYSCALE)
quicktime_template = cv.imread('./fish_assets/quicktime_template.png', cv.IMREAD_GRAYSCALE)
quicktime_directions = [ 
    config.RIGHT_STICK_UP, 
    config.RIGHT_STICK_DOWN,
    config.RIGHT_STICK_LEFT,
    config.RIGHT_STICK_RIGHT, 
    config.RIGHT_STICK_UP, 
    config.RIGHT_STICK_DOWN, 
    config.RIGHT_STICK_LEFT,
    config.RIGHT_STICK_RIGHT]

quicktime_positions = [
    [0, -23],
    [0, 23],
    [-23, 0],
    [23, 0],
    [0, -30],
    [0, 30],
    [-30, 0],
    [30, 0],    
]

exclamation_templates = [ 
    cv.imread('./fish_assets/exclamation1_template.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/exclamation2_template.png', cv.IMREAD_GRAYSCALE),
]

exclamation_masks = [ 
    cv.imread('./fish_assets/exclamation1_mask.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/exclamation2_mask.png', cv.IMREAD_GRAYSCALE),
]

fish_templates = [
    cv.imread('./fish_assets/fish1_template.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish2_template.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish3_template.png', cv.IMREAD_GRAYSCALE),
]

fish_masks = [
    cv.imread('./fish_assets/fish1_mask.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish2_mask.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish3_mask.png', cv.IMREAD_GRAYSCALE)
]


select_location()
select_total_fish()
select_runtime()


window = window_info.WindowInfo()

logging.info('Looking for chiaki window')
if not window.is_active():
    logging.info('Chiaki | Stream window not found')
    time.sleep(2.0)
    exit()
else:
    logging.info('Chiaki window found.')

background_thread = threading.Thread(target=program_timer, args=(TOTAL_RUNTIME,))
background_thread.start()

loop_time = time.time()

window_rect = { 
    'left' : 0,
    'top' : 0,
    'width' : window.content_width,
    'height' : window.content_height,
}

reel_rect = {
    'left' : 1140,
    'top' :  650,
    'width' : 23,
    'height' : 23,
}

complete_rect = {
    'left' : 929,
    'top' : 650,
    'width' : 26,
    'height' : 26,    
}

default_grab_rect = {}
default_grab_rect = { }
default_grab_rect['left'] = 570
default_grab_rect['top'] = 110
default_grab_rect['width'] = 160
default_grab_rect['height'] = 160

#keyboard_controller = Controller()

#screenshot.rect = window_rect
#5cv.namedWindow('Fish Tracker')
#window_info.focus()
time.sleep(0.2)
online_log.log("Starting bot", "w")
logging.info("Starting bot")
time.sleep(0.5)

#while True:
#    screen_colored = np.array(window.grab(window_rect))
#    draw_preview('Debug', screen_colored)  

while True:
    if bait_used == TOTAL_FISH:
        subprocess.run('python {}.py {} {}'.format(LOCATION_SCRIPT, TOTAL_FISH, SALVAGE_SELECTION))
        bait_used = 0

    bait_used += 1
    grab_rect = default_grab_rect.copy()
    time.sleep(1)
    online_log.log('Casting line: {}'.format(bait_used), 'a+')
    logging.info('Casting line: {}'.format(bait_used))
    window.key_press(config.R2, 2.1)
    waiting_for_hook = True

    online_log.log("Waiting for fish", 'a+')    
    logging.info("Waiting for fish")
    while(waiting_for_hook):
        screen_colored = np.array(window.grab(grab_rect))
        screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen_grab, hook_template, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            waiting_for_hook = False

        complete_screen = np.array(window.grab(complete_rect))
        complete_screen = cv.cvtColor(complete_screen, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(complete_screen, reel_template, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            online_log.log("Invalid location, moving camera", 'a+')             
            logging.info("Invalid location, moving camera")
            window.key_press(config.RIGHT_STICK_RIGHT, 0.2)
            break
        #draw_preview('Fish Tracker', screen_grab)
        #draw_preview('Debug', screen_colored)     
        loop_time = time.time()

    if not waiting_for_hook:
        online_log.log("Fish on!", 'a+')            
        logging.info("Fish on!")
        fish_on = True
        is_reel_pressed = True

        window.key_down(config.R2)
        cooldown = time.time() + 1
    else:
        continue

    while(fish_on):
        should_reel = False
        
        reel_screen = np.array(window.grab(reel_rect))
        screen_colored = np.array(window.grab(grab_rect))

        reel_screen = cv.cvtColor(reel_screen, cv.COLOR_BGR2GRAY)
        screen_grab = cv.cvtColor(screen_colored, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(reel_screen, reel_template, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        if locations:
            should_reel = True

        if should_reel:
            for (template, mask) in zip(fish_templates, fish_masks):    
                result = cv.matchTemplate(screen_grab, template, cv.TM_CCOEFF_NORMED, mask)
                locations = np.where(result >= 0.75)
                locations = list(zip(*locations[::-1]))
                if locations:
                    top_left = locations[0]
                    grab_rect['left'] = grab_rect['left'] + (top_left[0] + 19 - 80)
                    grab_rect['top'] = grab_rect['top'] + (top_left[1] + 19 - 80)         
                    bottom_right = (top_left[0] + 39, top_left[1] + 39)
                    cv.rectangle(screen_colored, top_left, bottom_right, (255, 0, 0), 2)
                    break
        else:
            # check fish completed
            complete_screen = np.array(window.grab(complete_rect))
            complete_screen = cv.cvtColor(complete_screen, cv.COLOR_BGR2GRAY)
            result = cv.matchTemplate(complete_screen, reel_template, cv.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.9)
            locations = list(zip(*locations[::-1]))
            if locations:
                online_log.log("Fish completed", 'a+')              
                logging.info("Fish completed")
                fish_on = False

            # check for r3 quicktime
            result = cv.matchTemplate(screen_grab, quicktime_template, cv.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.9)
            locations = list(zip(*locations[::-1]))
            if locations:
                top_left = locations[0]              
                grab_rect['left'] = grab_rect['left'] + (top_left[0] + 11 - 80)
                grab_rect['top'] = grab_rect['top'] + (top_left[1] + 8 - 80)         
                bottom_right = (top_left[0] + 22, top_left[1] + 16)
                cv.rectangle(screen_colored, top_left, bottom_right, (255, 0, 0), 2)
                center = [top_left[0] + 11, top_left[1] + 8]
                for (direction, position) in zip(quicktime_directions, quicktime_positions):
                    pixel_location = np.add(center, position)
                    if pixel_location[0] < 0 or pixel_location[0] >= 160 or pixel_location[1] < 0 or pixel_location[1] >= 160:
                        continue
                    b,g,r,a = screen_colored[pixel_location[1], pixel_location[0]]  
                    if r > 216 and g > 165 and b < 55:
                        logging.info("Press up: "+ str(direction))
                        window.key_press(direction, 0.05)
                        break                


            for (template, mask) in zip(exclamation_templates, exclamation_masks):           
                result = cv.matchTemplate(screen_grab, template, cv.TM_CCOEFF_NORMED, mask)
                locations = np.where(result >= 0.75)
                locations = list(zip(*locations[::-1]))
                if locations:
                    top_left = locations[0]
                    grab_rect['left'] = grab_rect['left'] + (top_left[0] + 19 - 80)
                    grab_rect['top'] = grab_rect['top'] + (top_left[1] + 19 - 80)         
                    bottom_right = (top_left[0] + 39, top_left[1] + 39)
                    cv.rectangle(screen_colored, top_left, bottom_right, (255, 0, 0), 2)
                    break

        if should_reel and not is_reel_pressed:
            window.key_down(config.R2)
            is_reel_pressed = True
            logging.info("Reel fish")
        elif not should_reel and is_reel_pressed and time.time() > cooldown:
            window.key_up(config.R2)
            is_reel_pressed = False
            logging.info("Pause reel")
            
        #draw_preview('Debug', reel_screen)     
        #draw_preview('Fish Tracker', screen_colored)
        loop_time = time.time()  


