from ewmh import EWMH
ewmh = EWMH()
client = None

def frame(client):
    frame = client
    while frame.query_tree().parent != ewmh.root:
        frame = frame.query_tree().parent
    return frame

def is_window_active():
    global client
    return client != None


for c in ewmh.getClientList():
    name = ewmh.getWmName(c)
    if name == 'Chiaki | Stream':
        client = c
        break


if client != None:
    geometry = frame(client).get_geometry()
    #print("Window: '{}' location x:{} y:{} width:{} height:{}".format(name, geometry.x, geometry.y, geometry.width, geometry.height))

#ewmh.setWmState(c, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
#ewmh.setWmState(c, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
#ewmh.setMoveResizeWindow(c, 0, 0, 0, 1081, 732)
#ewmh.display.flush()