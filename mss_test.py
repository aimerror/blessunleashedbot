import cv2 as cv
import numpy as np
from time import time
from mss import mss
import pyautogui

loop_time = time()



with mss() as sct:
    rect = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    while(True):

        screenshot = np.array(sct.grab(rect))
        #screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)

        cv.imshow('Computer Vision', screenshot)

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break


print('Done.')