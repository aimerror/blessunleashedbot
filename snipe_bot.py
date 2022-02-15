import window_info
import screenshot
import cv2 as cv
import numpy as np
import time
from mss import mss
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pytesseract

numbers = [
    cv.imread('./snipe_assets/0.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/1.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/2.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/3.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/4.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/5.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/6.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/7.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/8.jpg', cv.IMREAD_GRAYSCALE),
    cv.imread('./snipe_assets/9.jpg', cv.IMREAD_GRAYSCALE),
]

coordinates = [ 774, 765, 757, 744, 735, 726, 714, 705 ]

quality_list = [
    { 'name' : 'common', 'r' : 111, 'g' : 103, 'b' : 104 },
    { 'name' : 'uncommon', 'r' : 81, 'g' : 98, 'b' : 43 },
    { 'name' : 'rare', 'r' : 52, 'g' : 77, 'b' : 128 },
    { 'name' : 'epic', 'r' : 88, 'g' : 46, 'b' : 124 },
    { 'name' : 'legendary', 'r' : 120, 'g' : 109, 'b' : 36 }
]

items = [
    {
        "blessing" : 'valor',
        "character" : 'bezerker',
        "template" : cv.imread('./snipe_assets/epic_valor_bezerker.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'valor',
        "character" : 'crusader',
        "template" : cv.imread('./snipe_assets/epic_valor_crusader.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'valor',
        "character" : 'mage',
        "template" : cv.imread('./snipe_assets/epic_valor_mage.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'valor',
        "character" : 'priest',
        "template" : cv.imread('./snipe_assets/epic_valor_priest.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'valor',
        "character" : 'ranger',
        "template" : cv.imread('./snipe_assets/epic_valor_ranger.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'wolf',
        "character" : 'bezerker',
        "template" : cv.imread('./snipe_assets/wolf_bezerker.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'wolf',
        "character" : 'crusader',
        "template" : cv.imread('./snipe_assets/wolf_crusader.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'wolf',
        "character" : 'mage',
        "template" : cv.imread('./snipe_assets/wolf_mage.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'wolf',
        "character" : 'priest',
        "template" : cv.imread('./snipe_assets/wolf_priest.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'wolf',
        "character" : 'ranger',
        "template" : cv.imread('./snipe_assets/wolf_ranger.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'lion',
        "character" : 'bezerker',
        "template" : cv.imread('./snipe_assets/lion_bezerker.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'lion',
        "character" : 'crusader',
        "template" : cv.imread('./snipe_assets/lion_crusader.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'lion',
        "character" : 'mage',
        "template" : cv.imread('./snipe_assets/lion_mage.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'lion',
        "character" : 'priest',
        "template" : cv.imread('./snipe_assets/lion_priest.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'lion',
        "character" : 'ranger',
        "template" : cv.imread('./snipe_assets/lion_ranger.jpg', cv.IMREAD_GRAYSCALE)
    },        
    {
        "blessing" : 'crescent moon',
        "character" : 'bezerker',
        "template" : cv.imread('./snipe_assets/cm_bezerker.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'crescent moon',
        "character" : 'crusader',
        "template" : cv.imread('./snipe_assets/cm_crusader.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'crescent moon',
        "character" : 'mage',
        "template" : cv.imread('./snipe_assets/cm_mage.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'crescent moon',
        "character" : 'priest',
        "template" : cv.imread('./snipe_assets/cm_priest.jpg', cv.IMREAD_GRAYSCALE)
    },
    {
        "blessing" : 'crescent moon',
        "character" : 'ranger',
        "template" : cv.imread('./snipe_assets/cm_ranger.jpg', cv.IMREAD_GRAYSCALE)
    },     
]
# 165 552
window_rect = { 
    'left' : window_info.geometry.x + 10,
    'top' : window_info.geometry.y + 44,
    'width' : window_info.geometry.width - 20,
    'height' : window_info.geometry.height - 54,
}

selected_rect = {
    'left' : window_rect['left'] + 290,
    'top' : window_rect['top'] + 796,
    'width' : 25,
    'height' : 25,
}

price_rect = {
    'left' : window_rect['left'] + 687,
    'top' : window_rect['top'] + 819,
    'width' : 97,
    'height' : 26,    
}

def draw_preview(title, image):
    global window_rect
    cv.imshow(title, image)
    cv.moveWindow(title, window_rect['left'] + window_rect['width'], window_rect['top'])

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

sct = mss()

screenshot.rect = window_rect

custom_config = '--psm 13 -c tessedit_char_whitelist=0123456789'

while True:
        selected_screen = np.array(sct.grab(selected_rect))
        screen_grab = cv.cvtColor(selected_screen, cv.COLOR_BGR2GRAY)

        quality_name = None
        b,g,r,a = selected_screen[4, 1]
        precision = 10
        for quality in quality_list:
            if r > quality['r'] - precision and r < quality['r'] + precision and g > quality['g'] - precision and g < quality['g'] + precision and b > quality['b'] - precision and b < quality['b'] + precision:
                quality_name = quality['name']

        if quality_name == None:
            continue

        for item in items:
            result = cv.matchTemplate(screen_grab, item['template'], cv.TM_CCOEFF_NORMED)  
            locations = np.where(result >= 0.96)
            locations = list(zip(*locations[::-1]))
            if locations:
                price_string = ''
                for coordinate in coordinates:
                    price_rect = {
                        'left' : window_rect['left'] + coordinate - 1,
                        'top' : window_rect['top'] + 823,
                        'width' : 10,
                        'height' : 16,    
                    }
                    price_screen = cv.cvtColor(np.array(sct.grab(price_rect)), cv.COLOR_BGR2GRAY)
                    # cv.imshow('digit', price_screen)
                    # if cv.waitKey(1000) == ord('q'):
                    #     cv.destroyAllWindows()
                    #     exit()
                    for i in range(len(numbers)):
                        result = cv.matchTemplate(price_screen, numbers[i], cv.TM_CCOEFF_NORMED)
                        locations = np.where(result >= 0.83)
                        locations = list(zip(*locations[::-1]))
                        if locations:
                            #print("found "+ str(i) +" - "+ str(coordinate))
                            price_string = str(i) + price_string
                            break
                #print(price_string)
                #(thresh, blackAndWhiteImage) = cv.threshold(price_screen, 127, 255, cv.THRESH_BINARY)                
                #draw_preview('Price', blackAndWhiteImage)
                #price = pytesseract.image_to_string(price_screen, config=custom_config)
                #price = price.replace('\n', '').replace('\x0c', '')
                print("[{}] Item: {} {} [{}] Price: {}".format(time.strftime('%H:%M:%S'), item['blessing'], item['character'], quality_name, price_string))
                break
        time.sleep(0.1)