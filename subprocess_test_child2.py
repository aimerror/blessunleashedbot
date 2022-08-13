import time
import datetime
import log_message
import logging
import sys

if len(sys.argv) == 2:
    logging.info("child 2 reporting: "+ sys.argv[1])
    time.sleep(4.0)
    logging.info("child 2 ended")
else:
    logging.error("invalid parameter")