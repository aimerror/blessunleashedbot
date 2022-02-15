import window_info
import cv2 as cv
import numpy as np
import time
from mss import mss
import keyboard

sperios_direction = cv.imread('./fish_assets/fish_sperios.png', cv.IMREAD_GRAYSCALE)

window_rect = { 
    'left' : window_info.geometry.x + 10,
    'top' : window_info.geometry.y + 44,
    'width' : window_info.geometry.width - 20,
    'height' : window_info.geometry.height - 54,
}

minimap_rect = {
    'left' : window_rect['left'] + 1161,
    'top' : window_rect['top'] + 83,
    'width' : 40,
    'height' : 40,    
}

sct = mss()

ORANGE_MIN = np.array([20, 40, 180],np.uint8)
ORANGE_MAX = np.array([40, 70, 220],np.uint8)

#keyboard_controller = keyboard.Controller()
# time.sleep(3)
# keyboard_controller.press("l")
count = 1
time.sleep(3)
while True:
    original = sct.grab(minimap_rect)
    screen = np.array(original)  

    gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    thresh = cv.threshold(blurred, 150, 255, cv.THRESH_BINARY)[1]
    cv.imwrite('./screenshots/minimap_{}.png'.format(count), thresh)
    count += 1
   # result = cv.matchTemplate(thresh, sperios_direction, cv.TM_CCOEFF_NORMED)

  #  locations = np.where(result >= 0.75)
  #  locations = list(zip(*locations[::-1]))
  #  if locations:    
  #      print("found")
  #      keyboard_controller.release("l")
    #
    #frame_threshed = cv.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    #ret, thresh = cv.threshold(frame_threshed, 127, 255, 0)
    #contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #cv.drawContours(screen_colored, contours, -1, (0,255,0), 3)
    cv.imshow("Color Detected", thresh)
    if cv.waitKey(1000) == ord('q'):
        cv.destroyAllWindows()
        break
