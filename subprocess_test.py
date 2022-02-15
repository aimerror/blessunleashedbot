import time
import datetime
import subprocess
import log_message
import logging

TEST = 'hello'
logging.info("Starting child")
subprocess.run('python subprocess_test_child.py {}'.format(TEST))
logging.info("End")
