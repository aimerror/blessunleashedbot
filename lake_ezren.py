from asyncio import wait_for
import window_info
import cv2 as cv
import numpy as np
import time
import datetime
import config
import subprocess
import sys
import logging
import log_message
import online_log
import config

window = window_info.WindowInfo()

TOTAL_FISH = int(sys.argv[1]) if len(sys.argv) > 1 else 200
SALVAGE_SELECTION = int(sys.argv[2]) if len(sys.argv) > 2 else 20

loop_time = time.time()

window_rect = { 
    'left' : 0,
    'top' : 0,
    'width' : window.content_width,
    'height' : window.content_height,
}


lake_ezren_template = cv.imread('./fish_assets/lake_ezren_template.png', cv.IMREAD_GRAYSCALE)
lake_ezren_waypoint1_template = cv.imread('./fish_assets/lake_ezren_waypoint1.png', cv.IMREAD_GRAYSCALE)

minimap_rect = {
    'left' : 1110,
    'top' : 40,
    'width' : 130,
    'height' : 130,    
}

time.sleep(3.0)
##############
## TELEPORT ##
##############
online_log.log("Locating teleport", 'a+')    
logging.info("Locating teleport")
window.key_click(config.TOUCHPAD, 1.0)
window.key_click(config.DPAD_DOWN, 3.0)
window.key_press(config.CROSS, 1.0)
online_log.log("Teleporting...", 'a+')    
logging.info("Teleporting...")
time.sleep(7)

subprocess.run('python camera_sensitivity.py slow')
window.key_press(config.RIGHT_STICK_RIGHT, 2.9)
time.sleep(0.2)
subprocess.run('python camera_sensitivity.py default')
online_log.log("Running toward soulpyre", 'a+')    
logging.info("Running toward soulpyre")
reached_soul_pyre = False
window.key_down(config.LEFT_STICK_LEFT)
time.sleep(2.0)
window.key_down(config.LEFT_STICK_UP)

while not reached_soul_pyre:
    minimap = np.array(window.grab(minimap_rect))
    screen_grab = cv.cvtColor(minimap, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(screen_grab, lake_ezren_template, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.85)
    locations = list(zip(*locations[::-1]))
    if locations:
        top_left = locations[0]
        # print(top_left)
        #bottom_right = (top_left[0] + 19, top_left[1] + 18)
        # cv.rectangle(minimap, top_left, bottom_right, (255, 0, 0), 2)
        if top_left[1] >= 86:
            window.key_up(config.LEFT_STICK_UP)
        if top_left[0] >= 79:
            window.key_up(config.LEFT_STICK_LEFT)                     
            reached_soul_pyre = True
    time.sleep(0.1)

time.sleep(1)
# ########################
# ## salvage fish ########
# ########################
online_log.log("Starting salvage", 'a+')    
logging.info("Starting salvage")
subprocess.run('python salvage.py {} {}'.format(TOTAL_FISH, SALVAGE_SELECTION))
online_log.log("Salvage ended", 'a+')    
logging.info("Salvage ended")
# ########################
# ## walk to shopkeeper ##
# ########################
time.sleep(1.0)
online_log.log("Returning to fish spot", 'a+')    
logging.info("Returning to fish spot")
window.key_down(config.LEFT_STICK_UP)
window.key_down(config.LEFT_STICK_RIGHT)
time.sleep(3.0)
window.key_up(config.LEFT_STICK_UP)
time.sleep(9.0)
window.key_down(config.LEFT_STICK_UP)
time.sleep(4.0)
window.key_up(config.LEFT_STICK_RIGHT)
time.sleep(4.0)
window.key_press(config.LEFT_STICK_RIGHT, 1.0)
time.sleep(4.5)
window.key_press(config.LEFT_STICK_LEFT, 0.5)
time.sleep(3.0)
window.key_press(config.LEFT_STICK_LEFT, 1.5)
time.sleep(4.0)
window.key_press(config.LEFT_STICK_RIGHT, 0.5)
time.sleep(2.0)
window.key_up(config.LEFT_STICK_UP)

reached_waypoint_1 = False

window.key_down(config.LEFT_STICK_UP)
window.key_down(config.LEFT_STICK_LEFT)

while not reached_waypoint_1:
    minimap = np.array(window.grab(minimap_rect))
    screen_grab = cv.cvtColor(minimap, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(screen_grab, lake_ezren_waypoint1_template, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.85)
    locations = list(zip(*locations[::-1]))
    if locations:
        top_left = locations[0]
        #print(top_left)
        #bottom_right = (top_left[0] + 19, top_left[1] + 18)
        # cv.rectangle(minimap, top_left, bottom_right, (255, 0, 0), 2)
        if top_left[1] > 59:
            window.key_up(config.LEFT_STICK_UP)
            reached_waypoint_1 = True            
        if top_left[0] >= 93:
            window.key_up(config.LEFT_STICK_LEFT)
    time.sleep(0.1)
window.key_press(config.LEFT_STICK_LEFT, 1.0)
window.key_press(config.LEFT_STICK_UP, 10.0)
window.key_press(config.LEFT_STICK_RIGHT, 1.5)
window.key_press(config.LEFT_STICK_UP, 4.5)
window.key_press(config.LEFT_STICK_RIGHT, 9.7)
time.sleep(0.5)
window.key_press(config.RIGHT_STICK_RIGHT, 0.3)
online_log.log("Reached fishing spot", 'a+')    
logging.info("Reached fishing spot")
time.sleep(0.2)
window.key_click(config.SQUARE, 3.0)