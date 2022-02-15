import window_info
import screenshot

window_rect = { 
    'left' : window_info.geometry.x + 10,
    'top' : window_info.geometry.y + 44,
    'width' : window_info.geometry.width - 20,
    'height' : window_info.geometry.height - 54,
}

screenshot.rect = window_rect

while True:
    pass