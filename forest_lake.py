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

if not window_info.is_window_active():
    print('Chiaki | Stream window not found')

#TOTAL_FISH = int(sys.argv[1])
#SALVAGE_SELECTION = int(sys.argv[2])

loop_time = time.time()
sct = mss()
window_rect = { 
    'left' : window_info.x() + 10,
    'top' : window_info.y() + 31,
    'width' : window_info.width() - 20,
    'height' : window_info.height() - 39,
}

keyboard_controller = Controller()

downstream_teleport_template = cv.imread('./fish_assets/downstream_teleport.png', cv.IMREAD_GRAYSCALE)
soulpyre_template = cv.imread('./fish_assets/soulpyre_template.png', cv.IMREAD_GRAYSCALE)
soulpyre_mask = cv.imread('./fish_assets/soulpyre_mask.png', cv.IMREAD_GRAYSCALE)

check_map_rect = {
    'left' : window_rect['left'] + 615,
    'top' : window_rect['top'] + 335,
    'width' : 50,
    'height' : 50,
}

minimap_rect = {
    'left' : window_rect['left'] + 1110,
    'top' : window_rect['top'] + 40,
    'width' : 130,
    'height' : 130,    
}

time.sleep(3)

# keyboard_controller.press(Key.tab)
# time.sleep(0.1)
# keyboard_controller.release(Key.tab)
# time.sleep(1)

# wait_for_teleport = True
# while wait_for_teleport:
#     keyboard_controller.press(Key.left)
#     time.sleep(0.1)
#     keyboard_controller.release(Key.left)
#     time.sleep(1.0)

#     map_center = np.array(sct.grab(check_map_rect))
#     screen_grab = cv.cvtColor(map_center, cv.COLOR_BGR2GRAY)
#     result = cv.matchTemplate(screen_grab, downstream_teleport_template, cv.TM_CCOEFF_NORMED)
#     locations = np.where(result >= 0.9)
#     locations = list(zip(*locations[::-1]))
    
#     if locations:
#         wait_for_teleport = False

#     time.sleep(0.1)

# logging.info("Teleport found")
# time.sleep(1.0)
# keyboard_controller.press('g')
# time.sleep(1.0)
# keyboard_controller.release('g')

# time.sleep(7)

reached_soul_pyre = False
#keyboard_controller.press('d')
#keyboard_controller.press('s')
while not reached_soul_pyre:
    minimap = np.array(sct.grab(minimap_rect))
    screen_grab = cv.cvtColor(minimap, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(screen_grab, soulpyre_template, cv.TM_CCOEFF_NORMED, soulpyre_mask)
    locations = np.where(result >= 0.75)
    locations = list(zip(*locations[::-1]))
    if locations:
        top_left = locations[0]
        logging.info(top_left)
        bottom_right = (top_left[0] + 19, top_left[1] + 18)
        cv.rectangle(minimap, top_left, bottom_right, (255, 0, 0), 2)
        #if top_left[1] <= 67:
        #    keyboard_controller.release('s')
        #if top_left[0] <= 58:
        #    reached_soul_pyre = True
    cv.imshow("Test", minimap)
    cv.moveWindow('Test', window_rect['left'] + window_rect['width'] - 6, window_rect['top'] - 31)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()    
    time.sleep(0.1)
# keyboard_controller.release('d')
# keyboard_controller.press('s')
# time.sleep(2.4)
# keyboard_controller.release('s')
# time.sleep(2)
# ########################
# ## salvage fish ########
# ########################
# subprocess.run('python salvage.py {} {}'.format(TOTAL_FISH, SALVAGE_SELECTION))
# ########################
# ## walk to shopkeeper ##
# ########################
# time.sleep(2)
# keyboard_controller.press('d')
# time.sleep(0.5)
# keyboard_controller.release('d')
# keyboard_controller.press('s')
# time.sleep(1.5)
# keyboard_controller.release('s')
# keyboard_controller.press('a')
# time.sleep(0.4)
# keyboard_controller.release('a')
# time.sleep(1.0)
# ###################
# ## buy fish bait ##
# ###################
# subprocess.run('python buy_fish_bait.py {}'.format(TOTAL_FISH))
# ########################
# ## go to fishing spot ##
# ########################
# time.sleep(1)
# keyboard_controller.press('a')
# time.sleep(3)
# keyboard_controller.release('a')
# time.sleep(3)
# keyboard_controller.press('a')
# time.sleep(1)
# keyboard_controller.release('a')
# keyboard_controller.press('j')
# time.sleep(0.3)
# keyboard_controller.release('j')
# time.sleep(0.2)
# keyboard_controller.press('f')
# time.sleep(0.1)
# keyboard_controller.release('f')
# time.sleep(3)