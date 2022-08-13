import time
import datetime
import log_message
import logging
import sys
import subprocess

if len(sys.argv) == 2:
    logging.info("child reporting: "+ sys.argv[1])
    subprocess.run('python subprocess_test_child2.py {}'.format("child2"))    
    time.sleep(4.0)
    logging.info("child ended")
else:
    logging.error("invalid parameter")