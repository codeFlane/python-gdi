from win32gui import *
import win32con
import win32api
from __init__ import random_color, clean, get_cursor_pos, is_mouse_pressed, MouseButton, GDIdata
from random import randint
from enum import Enum
from icon import draw, extract, IconSourceDLL, ShellIcon
import ctypes
import win32ui

msimg32 = ctypes.windll.msimg32

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_byte),
        ("BlendFlags", ctypes.c_byte),
        ("SourceConstantAlpha", ctypes.c_byte),
        ("AlphaFormat", ctypes.c_byte)
    ]
def invert_colors(data, color=0xF0FFFF):
    """inverting colors"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    brush = CreateSolidBrush(color)
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def random_invert_colors(data):
    """inverting colors (randomly)"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    brush = CreateSolidBrush(random_color())
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def blur(data, offset=4, speed=70):
    """blur effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    mhdc = CreateCompatibleDC(hdc)
    hbit = CreateCompatibleBitmap(hdc, w, h)
    holdbit = SelectObject(mhdc, hbit)
    BitBlt(mhdc, 0, 0, w, h, hdc, 0, 0, win32con.SRCCOPY)
    AlphaBlend(hdc, randint(-offset, offset), randint(-offset, offset), w, h, mhdc, 0, 0, w, h, (0, 0, speed, 0))
    SelectObject(mhdc, holdbit)
    DeleteObject(holdbit)
    DeleteObject(hbit)
    DeleteDC(mhdc)

def radial_blur(data, lp_extra=30, speed=1000):
    """blur + rotate tunnel effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    mhdc = CreateCompatibleDC(hdc)
    hbit = CreateCompatibleBitmap(hdc, w, h)
    holdbit = SelectObject(mhdc, hbit)

    screen_size = GetWindowRect(GetDesktopWindow())

    left = screen_size[0]
    top = screen_size[1]
    right = screen_size[2]
    bottom = screen_size[3]
    if randint(0, 1):
        lppoint = ((left + lp_extra, top - lp_extra), (right + lp_extra, top + lp_extra), (left - lp_extra, bottom - lp_extra))
    else:
        lppoint = ((left - lp_extra, top + lp_extra), (right - lp_extra, top - lp_extra), (left + lp_extra, bottom + lp_extra))

    PlgBlt(mhdc, lppoint, hdc, left, top, (right - left), (bottom - top), 0, 0, 0)
    # BitBlt(mhdc, 0, 0, w, h, hdc, 0, 0, win32con.SRCCOPY)
    AlphaBlend(hdc, 0, 0, w, h, mhdc, 0, 0, w, h, (0, 0, speed, 0))
    SelectObject(mhdc, holdbit)
    DeleteObject(holdbit)
    DeleteObject(hbit)
    DeleteDC(mhdc)

class HatchBrushStyle(Enum):
    HORIZONTAL = 0 #horizontal lines
    VERTICAL = 1 #vertical lines
    RL_DIAGONAL = 2 #diagonal lines (from right bottom to left top)
    LR_DIAGONAL = 3 #diagonal lines (from left bottom to right top)
    RECT = 4 #horizontal & vertical lines
    DIAGONAL_RECT = 5 #left-right dialgonal & right-left diagonal lines
    RANDOM = 6 #random

def hatch_brush(data, style: HatchBrushStyle = HatchBrushStyle.RANDOM, set_bk_color=True):
    """inverting random colors + many lines"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    brush = CreateHatchBrush(style.value if style.value != 6 else randint(0, 5), random_color())
    if set_bk_color:
        SetBkColor(hdc, random_color())
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def color_filter(data, color):
    """color filter"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    brush = CreateSolidBrush(color)
    SelectObject(hdc, brush)
    BitBlt(hdc, 0, 0, w, h, hdc, 0, 0, win32con.MERGECOPY)
    DeleteObject(brush)

def random_color_filter(data):
    """random color filter"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    clean([w, h])
    brush = CreateSolidBrush(random_color())
    SelectObject(hdc, brush)
    BitBlt(hdc, 0, 0, w, h, hdc, 0, 0, win32con.MERGECOPY)
    DeleteObject(brush)

def tunnel(data, size=60):
    """copy window in small version that makes tunnel effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    StretchBlt(hdc, size, size, w - size * 2, h - size * 2, hdc, 0, 0, w, h, win32con.SRCCOPY)

def flip_v(data):
    """flip screen vertically"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    StretchBlt(hdc, 0, h, w, -h, hdc, 0, 0, w, h, win32con.SRCCOPY)

def flip_h(data):
    """flip screen horizontally"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    hdc, w, h = data.hdc, data.w, data.h
    StretchBlt(hdc, w, 0, -w, h, hdc, 0, 0, w, h, win32con.SRCCOPY)

def draw_icons_on_mouse(data, icon=extract(IconSourceDLL.SHELL, 0)):
    """draw icons behind mouse"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    hdc = data.hdc
    cursor = get_cursor_pos()
    draw(hdc, cursor[0], cursor[1], icon)

def draw_icons_on_clicked_mouse(data, button=MouseButton.LEFT, icon=extract(IconSourceDLL.SHELL, ShellIcon.STAR)):
    """draw icons behind mouse (only on click)"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    hdc = data.hdc, data.w, data.h
    if is_mouse_pressed(button):
        cursor = get_cursor_pos()
        draw(hdc, cursor[0], cursor[1], icon)

def random_errors(data, icon=LoadIcon(None, win32con.IDI_ERROR)):
    """draw icons on screen randomly"""
    #by Leo-Aqua
    hdc, w, h = data.hdc, data.w, data.h
    DrawIcon(hdc, randint(0, w), randint(0, h), icon)

def time_color_filter(data, t):
    """add color filter using current time (requires time)"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    brush = CreateSolidBrush(win32api.RGB(t % 256, (t // 2) % 256, (t // 2) % 256))
    old = SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    SelectObject(hdc, old)
    DeleteObject(brush)

def time_resize(data, t):
    """resize using current time (requires time)"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    t *= 10
    BitBlt(hdc, 0, 0, w, h, hdc, t % w, t % h, win32con.NOTSRCERASE)

def pixelization(data):
    """pixelate your screen"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    hdc_mem = CreateCompatibleDC(hdc)
    hbitmap = CreateCompatibleBitmap(hdc, w, h)
    old = SelectObject(hdc_mem, hbitmap)
    BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, win32con.SRCCOPY)
    for i in range(0, w // 10):
        for j in range(0, h // 10):
            StretchBlt(hdc_mem, i * 10, j * 10, 10, 10, hdc_mem, i * 10, j * 10, 1, 1, win32con.SRCCOPY)
    BitBlt(hdc, 0, 0, w, h, hdc_mem, 0, 0, win32con.SRCCOPY)
    SelectObject(hdc_mem, old)
    DeleteObject(hbitmap)
    DeleteDC(hdc_mem)

def random_text(data, text='HYDROGEN', count=1):
    """add text with random position, color and background. You can add custom text using "text" keyword argument. You can also increase
    count of text adding per call using "count" keyword argument"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    hdc_mem = CreateCompatibleDC(hdc)
    hbitmap = CreateCompatibleBitmap(hdc, w, h)
    old = SelectObject(hdc_mem, hbitmap)
    dc = win32ui.CreateDCFromHandle(hdc)
    BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, win32con.SRCCOPY)
    SetBkColor(hdc, win32api.RGB(randint(0,255), randint(0,255), randint(0,255)))
    SetTextColor(hdc, win32api.RGB(randint(0,255), randint(0,255), randint(0,255)))
    for _ in range(count):
        dc.TextOut(randint(0, w), randint(0, h), text)
    blend = BLENDFUNCTION(0, 0, 128, 0)
    msimg32.AlphaBlend(hdc, 0, 0, w, h, hdc_mem, 0, 0, w, h, blend)
    SelectObject(hdc_mem, old)
    DeleteObject(hbitmap)
    DeleteDC(hdc_mem)

def rotate_3d(data):
    """rotate your screen like 3d"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    points = [(0, 0), (w, 0), (25, h)]
    PlgBlt(hdc, points, hdc, 0, 0, w + 25, h, None, 0, 0)

def random_circles_rects(data, t, text="     "):
    """draw black-white circles and rects in random position (requires time). You can add text to rect using "text" keyword argument"""
    #by LeoLezury (from Hydrogen source code)
    hdc, w, h = data.hdc, data.w, data.h
    t *= 30
    RedrawWindow(None, None, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE | win32con.RDW_ALLCHILDREN)
    hdc_mem = CreateCompatibleDC(hdc)
    hbitmap = CreateCompatibleBitmap(hdc, w, h)
    old = SelectObject(hdc_mem, hbitmap)
    dc = win32ui.CreateDCFromHandle(hdc)
    BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, win32con.NOTSRCCOPY)
    brush = CreatePatternBrush(hbitmap)
    old_brush = SelectObject(hdc, brush)
    for i in range(3):
        Ellipse(hdc, t % w + 10*i, t % h + 10*i, t % w + 200 - 10*i, t % h + 200 - 10*i)
    for i in range(5):
        dc.TextOut(randint(0, w), randint(0, h), text)
    SelectObject(hdc, old_brush)
    DeleteObject(brush)
    SelectObject(hdc_mem, old)
    DeleteObject(hbitmap)
    DeleteDC(hdc_mem)
