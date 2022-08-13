import time
import sys
import window_info
import config

TOTAL_FISH = int(sys.argv[1])
SALVAGE_SELECTION = int(sys.argv[2])

window = window_info.WindowInfo()

time.sleep(2.0)
window.key_click(config.SQUARE, 1.0)
window.key_click(config.CROSS, 2.0)

steps = int(TOTAL_FISH / SALVAGE_SELECTION)

for current_step in range(steps):
    for slot in range(SALVAGE_SELECTION):
        window.key_click(config.CROSS, 0.2)
        window.key_click(config.DPAD_DOWN, 0.2)

    window.key_press(config.CROSS, 1.0)
    time.sleep(0.5)
    window.key_click(config.CROSS, 2.0)

window.key_click(config.CIRCLE, 0.5)
window.key_click(config.CIRCLE, 1.0)