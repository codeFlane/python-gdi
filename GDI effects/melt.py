import win32gui
import win32con
from random import randint
from __init__ import GDIinfo

def melt(info: GDIinfo):
    """make your screen melt"""
    w, h = info.w, info.h
    x = 0
    while True:
        hdc = win32gui.GetDC(0)
        x = randint(0, w)
        win32gui.BitBlt(hdc, x, 1, 10, h, hdc, x, 0, win32con.SRCCOPY)
        win32gui.ReleaseDC(0, hdc)
