import time
import window_info
import config
import sys

sensitivity = sys.argv[1] if len(sys.argv) > 1 else 'default'

window = window_info.WindowInfo()

time.sleep(1.0)
window.key_click(config.OPTIONS, 1.0)
window.key_click(config.SQUARE, 1.0)
window.key_click(config.CROSS, 1.0)
window.key_click(config.CROSS, 1.0)

for i in range(5):
    window.key_click(config.DPAD_DOWN, 0.1)

if sensitivity == 'slow':
    window.key_press(config.DPAD_LEFT, 1.5)
else:
    for i in range(24):
        window.key_click(config.DPAD_RIGHT, 0.05)

time.sleep(0.5)

window.key_click(config.CIRCLE, 1.0)
window.key_click(config.CIRCLE, 2.0)