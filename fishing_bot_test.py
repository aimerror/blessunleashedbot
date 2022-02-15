import window_info
import cv2 as cv
import numpy as np
from time import time
from mss import mss

hotspots = [
    cv.imread('./fish_assets/hotspot_01.png'),
    cv.imread('./fish_assets/hotspot_02.png'),
    cv.imread('./fish_assets/hotspot_03.png'),        
]
screen_colored = cv.imread('./screenshots/ss_3.png')

window_rect = { 
    'left' : window_info.geometry.x + 10,
    'top' : window_info.geometry.y + 44,
    'width' : window_info.geometry.width - 20,
    'height' : window_info.geometry.height - 54,
}

sct = mss()

ORANGE_MIN = np.array([100, 40, 170],np.uint8)
ORANGE_MAX = np.array([120, 255, 255],np.uint8)

while True:
    original = sct.grab(window_rect)
    screen = np.array(original)  
    hsv_img = cv.cvtColor(screen, cv.COLOR_BGR2HSV)
    frame_threshed = cv.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    #ret, thresh = cv.threshold(frame_threshed, 127, 255, 0)
    #contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #cv.drawContours(screen_colored, contours, -1, (0,255,0), 3)
    cv.imshow("Color Detected", frame_threshed)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
