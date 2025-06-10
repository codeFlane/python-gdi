import win32gui
import win32con
import math
from __init__ import GDIinfo

def shake(info: GDIinfo, angle: int = 0, size: int = 1, speed: int = 5):
    """shake/pan your screen"""
    hdc, w, h = info.hdc, info.w, info.h
    dx = dy = 1
    angle = angle
    size = size
    speed = speed
    while True:
        win32gui.BitBlt(hdc, 0, 0, w, h, hdc, dx, dy, win32con.SRCCOPY)
        dx = math.ceil(math.sin(angle) * size * 10)
        dy = math.ceil(math.cos(angle) * size * 10)
        angle += speed / 10
        if angle > math.pi :
            angle = math.pi * -1
