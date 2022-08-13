from multiprocessing.connection import wait
import threading
import time
import datetime
import subprocess
import log_message
import logging
import os

wait_time=2

def program_timer(wt):
    countdown = wt
    while countdown > 0:
        logging.info('closing program in {0} {1}'.format(countdown, 'minute' if countdown == 1 else 'minutes'))
        time.sleep(5)
        countdown -= 1

    
    time.sleep(wt)
    logging.info('closing program')
    os._exit(1)

background_thread = threading.Thread(target=program_timer, args=(wait_time,))
background_thread.start()
logging.info('hello 1')
time.sleep(4)
logging.info('hello 2')
time.sleep(4)
logging.info('hello 3')
