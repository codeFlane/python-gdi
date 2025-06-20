import win32gui
import win32con
from __init__ import GDIinfo
from random import randint

def errors(info: GDIinfo, icon: int = win32con.IDI_ERROR):
    """fill your screen in icons"""
    hdc, w, h = info.hdc, info.w, info.h
    x = y = 0
    while True:
        win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, icon))
        x = x + 30
        if x >= w:
            y = y + 30
            x = 0
        if y >= h:
            x = y = 0

def random_errors(info: GDIinfo, icon: int = win32con.IDI_ERROR):
    "fill your screen in icons (random position)"
    hdc, w, h = info.hdc, info.w, info.h
    while True:
        win32gui.DrawIcon(hdc, randint(0, w), randint(0, h), win32gui.LoadIcon(None, icon))