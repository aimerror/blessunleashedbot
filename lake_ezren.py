from asyncio import wait_for
import window_info
import screenshot
import cv2 as cv
import numpy as np
import time
import datetime
from mss import mss
from pynput import keyboard
from pynput.keyboard import Key, Controller
import subprocess
import sys
import logging
import log_message
import online_log

if not window_info.is_window_active():
    print('Chiaki | Stream window not found')

window_info.focus()

TOTAL_FISH = int(sys.argv[1]) if len(sys.argv) > 1 else 200
SALVAGE_SELECTION = int(sys.argv[2]) if len(sys.argv) > 2 else 20

loop_time = time.time()
sct = mss()
window_rect = { 
    'left' : window_info.x() + 10,
    'top' : window_info.y() + 31,
    'width' : window_info.width() - 20,
    'height' : window_info.height() - 39,
}

keyboard_controller = Controller()

lake_ezren_template = cv.imread('./fish_assets/lake_ezren_template.png', cv.IMREAD_GRAYSCALE)
lake_ezren_waypoint1_template = cv.imread('./fish_assets/lake_ezren_waypoint1.png', cv.IMREAD_GRAYSCALE)

minimap_rect = {
    'left' : window_rect['left'] + 1110,
    'top' : window_rect['top'] + 40,
    'width' : 130,
    'height' : 130,    
}

time.sleep(3.0)
##############
## TELEPORT ##
##############
online_log.log("Locating teleport", 'a+')    
logging.info("Locating teleport")
keyboard_controller.press(Key.tab)
time.sleep(0.1)
keyboard_controller.release(Key.tab)
time.sleep(1)

keyboard_controller.press(Key.down)
time.sleep(0.1)
keyboard_controller.release(Key.down)
time.sleep(3.0)
keyboard_controller.press('g')
time.sleep(1.0)
keyboard_controller.release('g')
online_log.log("Teleporting...", 'a+')    
logging.info("Teleporting...")
time.sleep(7)

subprocess.run('python camera_sensitivity.py slow')
keyboard_controller.press('l')
time.sleep(2.9)
keyboard_controller.release('l')
time.sleep(0.2)
subprocess.run('python camera_sensitivity.py default')
online_log.log("Running toward soulpyre", 'a+')    
logging.info("Running toward soulpyre")
reached_soul_pyre = False
keyboard_controller.press('a')
time.sleep(2.0)
keyboard_controller.press('w')

while not reached_soul_pyre:
    minimap = np.array(sct.grab(minimap_rect))
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
            keyboard_controller.release('w')
        if top_left[0] >= 79:
            keyboard_controller.release('a')            
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
keyboard_controller.press('w')
keyboard_controller.press('d')
time.sleep(3.0)
keyboard_controller.release('w')
time.sleep(9.0)
keyboard_controller.press('w')
time.sleep(4.0)
keyboard_controller.release('d')
time.sleep(4.0)
keyboard_controller.press('d')
time.sleep(1.0)
keyboard_controller.release('d')
time.sleep(4.5)
keyboard_controller.press('a')
time.sleep(0.5)
keyboard_controller.release('a')
time.sleep(3.0)
keyboard_controller.press('a')
time.sleep(1.5)
keyboard_controller.release('a')
time.sleep(4.0)
keyboard_controller.press('d')
time.sleep(0.5)
keyboard_controller.release('d')
time.sleep(2.0)
keyboard_controller.release('w')

reached_waypoint_1 = False

keyboard_controller.press('w')
keyboard_controller.press('a')

while not reached_waypoint_1:
    minimap = np.array(sct.grab(minimap_rect))
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
            keyboard_controller.release('w')
            reached_waypoint_1 = True            
        if top_left[0] >= 93:
            keyboard_controller.release('a')            
    time.sleep(0.1)
keyboard_controller.press('a')
time.sleep(1.0)
keyboard_controller.release('a')
keyboard_controller.press('w')
time.sleep(10.0)
keyboard_controller.release('w')
keyboard_controller.press('d')
time.sleep(1.5)
keyboard_controller.release('d')
keyboard_controller.press('w')
time.sleep(4.5)
keyboard_controller.release('w')
keyboard_controller.press('d')
time.sleep(9.7)
keyboard_controller.release('d')
time.sleep(0.5)
keyboard_controller.press('l')
time.sleep(0.3)
keyboard_controller.release('l')
online_log.log("Reached fishing spot", 'a+')    
logging.info("Reached fishing spot")
time.sleep(0.2)
keyboard_controller.press('f')
time.sleep(0.1)
keyboard_controller.release('f')
time.sleep(3)