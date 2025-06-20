import win32gui
from __init__ import GDIinfo
from time import sleep

def rotate_tunnel(info: GDIinfo, delay: float = 0.01, side: str = 'left'):
    hdc = info.hdc
    screen_size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())

    left = screen_size[0]
    top = screen_size[1]
    right = screen_size[2]
    bottom = screen_size[3]
    if side == 'left':
        lpppoint = ((left + 50, top - 50), (right + 50, top + 50), (left - 50, bottom - 50))
    if side == 'right':
        lpppoint = ((left - 50, top + 50), (right - 50, top - 50), (left + 50, bottom + 50))

    for i in range(10):
        win32gui.PlgBlt(hdc, lpppoint, hdc, left - 20, top - 20, (right - left) + 40, (bottom - top) + 40, None, 0, 0)
        sleep(delay)