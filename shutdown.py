import window_info
import time
import config
import logging
import online_log
import os

window = window_info.WindowInfo()
time.sleep(1.0)

def reset_controls():
    controls = [ config.TOUCHPAD, config.DPAD_DOWN, config.DPAD_LEFT, config.DPAD_RIGHT, config.DPAD_UP, config.LEFT_STICK_DOWN, config.LEFT_STICK_LEFT, config.LEFT_STICK_RIGHT, config.LEFT_STICK_UP, config.CIRCLE, config.CROSS ]
    for button in controls:
        window.key_click(button, 0.1)

if window.is_active():
    reset_controls()
    print("")
    time.sleep(1.0)
    online_log.log("shutting down playstation", 'a+')
    logging.info("shutting down playstation")
    window.key_click(config.PS, 2.0)
    window.key_click(config.DPAD_DOWN, 1.0)
    window.key_click(config.DPAD_LEFT, 1.0)
    window.key_click(config.CROSS, 1.0)
    window.key_click(config.DPAD_DOWN, 1.0)
    window.key_click(config.CROSS, 1.0)
    time.sleep(1.0)

online_log.log("shutting down PC", 'a+')
logging.info("shutting down PC")
os.system("shutdown /s /t 1")