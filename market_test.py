import PIL
import time
import pygetwindow
import pyautogui
import cv2
import numpy as np
from pynput.keyboard import KeyCode, Key, Controller
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

R1 = KeyCode(99)
SQUARE = KeyCode(100)
CIRCLE = KeyCode(102)
CROSS = KeyCode(98)
TRIANGLE = KeyCode(104)

D_PAD_DOWN = KeyCode(40)

window = pygetwindow.getWindowsWithTitle('Chiaki | Stream')[0]
window.left = 740
window.top = 0
window.size = (1820, 1057)

time.sleep(0.5)
window.activate()
time.sleep(0.5)

print("Opening market place")
keyboard = Controller()

keyboard.press(SQUARE)
time.sleep(0.1)
keyboard.release(SQUARE)
time.sleep(2.0)
keyboard.press(CROSS)
time.sleep(0.1)
keyboard.release(CROSS)
time.sleep(2.0)
keyboard.press(CROSS)
time.sleep(0.1)
keyboard.release(CROSS)
time.sleep(1.0)
keyboard.press(R1)
time.sleep(0.1)
keyboard.release(R1)
time.sleep(0.5)
for i in range(8):
    keyboard.press(D_PAD_DOWN)
    time.sleep(0.1)
    keyboard.release(D_PAD_DOWN)
    time.sleep(0.1)

keyboard.press(CROSS)
time.sleep(0.1)
keyboard.release(CROSS)
time.sleep(1.0)
keyboard.press(D_PAD_DOWN)
time.sleep(0.1)
keyboard.release(D_PAD_DOWN)
time.sleep(0.1)
keyboard.press(CROSS)
time.sleep(0.1)
keyboard.release(CROSS)

time.sleep(1.5)
for i in range(7):
    keyboard.press(D_PAD_DOWN)
    time.sleep(0.1)
    keyboard.release(D_PAD_DOWN)
    time.sleep(0.1)

time.sleep(0.1)
print("Getting items and prices")
capture = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
capture = cv2.cvtColor(np.array(capture), cv2.COLOR_BGR2GRAY)
products = capture[300:890, 295:630] #320, 320, 340, 590
product_totals = []
products_cheapest = []
#cv2.imshow('Price', products)
#cv2.waitKey(0)
text = pytesseract.image_to_string(products)
text = text.rstrip()
entries = text.split('\n\n')
number_of_entries = len(entries)
custom_config = r'--psm 6  -c tessedit_char_whitelist=0123456789.'
for x in range(number_of_entries):
    product_total = capture[310+x*83:340+x*83, 635:790]
    text = pytesseract.image_to_string(product_total)
    number = text.split(' ')[1]
    product_totals.append(number)

    product_price = capture[336+x*83:368+x*83, 635:745]
    #cv2.imshow('Price', product_price)
    #cv2.waitKey(0)    
    text = pytesseract.image_to_string(product_price, config=custom_config)
    text = text.replace('\n', '').replace('\x0c', '')
    products_cheapest.append(text)


for i in range(number_of_entries):
    print("Name: {: <20} Number of Items: {: <6} Cheapest: {: >7}".format(entries[i], product_totals[i], "$" + products_cheapest[i]))
