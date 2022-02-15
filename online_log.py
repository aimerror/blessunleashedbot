import requests
import threading
import datetime
import logging
import log_message

def log(message, flag):
    t = threading.Thread(target=_send, args=(message, flag))
    t.start()

def _send(message, flag):
    x = datetime.datetime.now()
    date_time = x.strftime("%Y-%m-%d, %H:%M:%S")

    url = 'https://bu-fish-log.glitch.me/'
    myobj = {
        "api_key": "1522de88-d6cf-40b0-be54-9a4222e942fa",
        "message": "[{}] {}\n".format(date_time, message),
        "flag": flag
    }

    x = requests.post(url, data = myobj)
    logging.info("{} ({})".format(message, x.status_code))

# log_online('Test message', 'w')