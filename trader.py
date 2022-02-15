import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'



img = cv2.imread('D:/screen2.PNG')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

products = img[320:910, 320:660] #320, 320, 340, 590
cv2.imshow('Price', products)
cv2.waitKey(0)
product_totals = []
products_cheapest = []

text = pytesseract.image_to_string(products)
text = text.rstrip()
entries = text.split('\n\n')
number_of_entries = len(entries)
custom_config = r'--psm 6  -c tessedit_char_whitelist=0123456789.'
for x in range(number_of_entries):
    product_total = img[328+x*86:352+x*86, 675:835]
    text = pytesseract.image_to_string(product_total)
    number = text.split(' ')[1]
    product_totals.append(number)

    product_price = img[352+x*86:380+x*86, 675:790]
    text = pytesseract.image_to_string(product_price, config=custom_config)
    text = text.replace('\n', '').replace('\x0c', '')
    #print(repr(text))
    #cv2.imshow('Price', product_price)
    #cv2.waitKey(0)
    products_cheapest.append(text)


for i in range(number_of_entries):
    print("Name: {: <20} Number of Items: {: <6} Cheapest: {: >7}".format(entries[i], product_totals[i], "$" + products_cheapest[i]))


