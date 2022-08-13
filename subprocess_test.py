import threading
import time
import datetime
import subprocess
import log_message
import logging
import os
import signal
import atexit
import sys
import psutil

wait_time=2


def cleanup():
    print("checking processes")
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        print('Child pid is {}'.format(child.pid))
        os.kill(child.pid, signal.SIGTERM)
    os._exit(1)

    

def program_timer():
    time.sleep(2.0)
    logging.info('closing program')
    cleanup()


background_thread = threading.Thread(target=program_timer)
background_thread.start()


TEST = 'hello'
logging.info("Starting child")
process = subprocess.run('python subprocess_test_child.py {}'.format(TEST))
logging.info("End")

