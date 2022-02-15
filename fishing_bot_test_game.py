import window_info
import cv2 as cv
import numpy as np
from time import time
import mss
import mss.tools

hook_template = cv.imread('./fish_assets/hook_template.png', cv.IMREAD_GRAYSCALE)
fish_templates = [
    cv.imread('./fish_assets/fish1_template.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish2_template.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish3_template.png', cv.IMREAD_GRAYSCALE),
]

fish_masks = [
    cv.imread('./fish_assets/fish1_mask.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish2_mask.png', cv.IMREAD_GRAYSCALE),
    cv.imread('./fish_assets/fish3_mask', cv.IMREAD_GRAYSCALE)
]

screen = cv.imread('./screenshots/ss_8.png')

if not window_info.is_window_active():
    print('Chiaki | Stream window not found')

window_rect = { 
    'left' : window_info.geometry.x + 10,
    'top' : window_info.geometry.y + 44,
    'width' : window_info.geometry.width - 20,
    'height' : window_info.geometry.height - 54,
}

grab_rect = { }
grab_rect['left'] = window_rect['left'] + 570
grab_rect['top'] = window_rect['top'] + 110
grab_rect['width'] = 140
grab_rect['height'] = 140

loop_time = time()
sct = mss.mss()

needle_w = 39
needle_h = 39
count = 0
while(True):
    original = sct.grab(grab_rect)
    screen = np.array(original)    
    screen_grab = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    for (template, mask) in zip(fish_templates, fish_masks):    
        result = cv.matchTemplate(screen_grab, template, cv.TM_CCOEFF_NORMED, mask)
        locations = np.where(result >= 0.65)
        locations = list(zip(*locations[::-1]))
        if locations:
            top_left = locations[0]
            grab_rect['left'] = grab_rect['left'] + (top_left[0] + 19 - 70)
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
            cv.rectangle(screen, top_left, bottom_right, (0, 255, 255), 2)
            break

    font = cv.FONT_HERSHEY_SIMPLEX
    org = (5, 15)
    font_scale = 0.5
    color = (255, 255, 255)  
    thickness = 1
    framerate = 'FPS {}'.format(int(1 / (time() - loop_time)))
    screen_grab = cv.putText(screen, framerate, org, font, font_scale, color, thickness, cv.LINE_AA)    
    cv.imshow('Fish Tracker', screen_grab)

    loop_time = time()  

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
