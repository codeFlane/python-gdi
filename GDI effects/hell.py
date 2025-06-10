import win32gui
import win32con
from random import randrange, randint
import colorsys
import win32api
from __init__ import GDIinfo
from time import sleep

def bw_hell(info: GDIinfo, delay: float = 0.01, shake: int = 4):
    """add black-white color filters with linees and shaking"""
    hdc, w, h = info.hdc, info.w, info.h
    while True:
        win32gui.BitBlt(hdc, 0, 0, w, h, hdc, randrange(-shake, shake), randrange(-shake, shake), win32con.NOTSRCCOPY)
        sleep(delay)

def rb_hell(info: GDIinfo, delay: float = 0.01, shake: int = 10):
    """add color filters to your window and shake it"""
    hdc, w, h = info.hdc, info.w, info.h
    color = 0
    while True:
        rgb_color = colorsys.hsv_to_rgb(color, 1.0, 1.0)
        brush = win32gui.CreateSolidBrush(
            win32api.RGB(
                int(rgb_color[0]) * 255, int(rgb_color[1]) * 255, int(rgb_color[2]) * 255
            )
        )
        win32gui.SelectObject(hdc, brush)
        win32gui.BitBlt(hdc, randint(-shake, shake), randint(-shake, shake), w, h, hdc, 0, 0, win32con.SRCCOPY)
        win32gui.BitBlt(hdc, randint(-shake, shake), randint(-shake, shake), w, h, hdc, 0, 0, win32con.PATINVERT)
        color += 0.05
        sleep(delay)