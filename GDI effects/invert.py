import win32gui
from time import sleep
from __init__ import GDIinfo

def invert(info: GDIinfo, delay: float = 0.2):
    """invert colors on your window

    Args:
        info (GDIinfo): info
        delay (float, optional): delay updating. Defaults to 0.2.
    """
    hdc, w, h = info.hdc, info.w, info.h
    while True:
        win32gui.InvertRect(hdc, (0, 0, w, h))
        sleep(delay)
