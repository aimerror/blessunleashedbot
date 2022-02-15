import time
import datetime
import log_message
import logging
import sys

if len(sys.argv) == 2:
    logging.info("child reporting: "+ sys.argv[1])
    time.sleep(2.0)
    logging.info("child ended")
else:
    logging.error("invalid parameter")