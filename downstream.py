import window_info
import cv2 as cv
import numpy as np
import time
import datetime
import subprocess
import sys
import logging
import log_message
import online_log
import config

window = window_info.WindowInfo()

TOTAL_FISH = int(sys.argv[1])
SALVAGE_SELECTION = int(sys.argv[2])

loop_time = time.time()

window_rect = { 
    'left' : 0,
    'top' : 0,
    'width' : window.content_width,
    'height' : window.content_height,
}

downstream_teleport_template = cv.imread('./fish_assets/downstream_teleport.png', cv.IMREAD_GRAYSCALE)
soulpyre_template = cv.imread('./fish_assets/soulpyre_template.png', cv.IMREAD_GRAYSCALE)
soulpyre_mask = cv.imread('./fish_assets/soulpyre_mask.png', cv.IMREAD_GRAYSCALE)

check_map_rect = {
    'left' : 615,
    'top' : 335,
    'width' : 50,
    'height' : 50,
}

minimap_rect = {
    'left' : 1110,
    'top' : 40,
    'width' : 130,
    'height' : 130,    
}

time.sleep(3)
online_log.log("Locating teleport", 'a+')    
logging.info("Locating teleport")
window.key_press(config.TOUCHPAD, 0.1)
time.sleep(1)

wait_for_teleport = True
while wait_for_teleport:
    window.key_press(config.DPAD_LEFT, 0.1)
    time.sleep(1.0)

    map_center = np.array(window.grab(check_map_rect))
    screen_grab = cv.cvtColor(map_center, cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(screen_grab, downstream_teleport_template, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= 0.9)
    locations = list(zip(*locations[::-1]))
    
    if locations:
        wait_for_teleport = False

    time.sleep(0.1)

logging.info("Teleport found")
time.sleep(1.0)
window.key_press(config.CROSS, 1.0)
online_log.log("Teleporting...", 'a+')    
logging.info("Teleporting...")
time.sleep(7)
online_log.log("Running toward soulpyre", 'a+')    
logging.info("Running toward soulpyre")
window.key_down(config.LEFT_STICK_RIGHT)
time.sleep(7)
window.key_press(config.LEFT_STICK_DOWN, 1.5)
time.sleep(4)
window.key_press(config.LEFT_STICK_DOWN, 3.0)
time.sleep(5)
window.key_press(config.LEFT_STICK_DOWN, 1.5)
time.sleep(4)
window.key_up(config.LEFT_STICK_RIGHT)

reached_soul_pyre = False
window.key_down(config.LEFT_STICK_RIGHT)
window.key_down(config.LEFT_STICK_DOWN)
while not reached_soul_pyre:
    minimap = np.array(window.grab(minimap_rect))
    screen_grab = cv.cvtColor(minimap, cv.COLOR_BGR2GRAY)
    #draw_preview('minimap', minimap)
    result = cv.matchTemplate(screen_grab, soulpyre_template, cv.TM_CCOEFF_NORMED, soulpyre_mask)
    locations = np.where(result >= 0.75)
    locations = list(zip(*locations[::-1]))
    if locations:
        top_left = locations[0]
        bottom_right = (top_left[0] + 19, top_left[1] + 18)
        cv.rectangle(minimap, top_left, bottom_right, (255, 0, 0), 2)
        if top_left[1] <= 67:
            window.key_up(config.LEFT_STICK_DOWN)
        if top_left[0] <= 58:
            reached_soul_pyre = True
    time.sleep(0.1)

window.key_up(config.LEFT_STICK_RIGHT)
window.key_press(config.LEFT_STICK_DOWN, 2.4)

time.sleep(2)
########################
## salvage fish ########
########################
online_log.log("Starting salvage", 'a+')    
logging.info("Starting salvage")
subprocess.run('python salvage.py {} {}'.format(TOTAL_FISH, SALVAGE_SELECTION))
online_log.log("Salvage ended", 'a+')    
logging.info("Salvage ended")
########################
## walk to shopkeeper ##
########################
time.sleep(2)
online_log.log("Returning to fish spot", 'a+')    
logging.info("Returning to fish spot")
window.key_press(config.LEFT_STICK_RIGHT, 0.5)
window.key_press(config.LEFT_STICK_DOWN, 1.5)
window.key_press(config.LEFT_STICK_LEFT, 0.4)
time.sleep(1.0)
###################
## buy fish bait ##
###################
#subprocess.run('python buy_fish_bait.py {}'.format(TOTAL_FISH))
########################
## go to fishing spot ##
########################
time.sleep(1)
window.key_press(config.LEFT_STICK_LEFT, 3.0)
time.sleep(3)
window.key_press(config.LEFT_STICK_LEFT, 1.0)
window.key_press(config.RIGHT_STICK_LEFT, 0.3)
time.sleep(0.2)
online_log.log("Reached fishing spot", 'a+')    
logging.info("Reached fishing spot")
window.key_press(config.SQUARE, 0.1)
time.sleep(3)