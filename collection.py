from win32gui import *
import win32con
from __init__ import random_color, clean, get_cursor_pos, is_mouse_pressed, MouseButton
from random import randint
from enum import Enum
from icon import draw, extract, IconSourceDLL, ShellIcon

def invert_colors(hdc, w, h, color=0xF0FFFF):
    """inverting colors"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    brush = CreateSolidBrush(color)
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def random_invert_colors(hdc, w, h):
    """inverting colors (randomly)"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    brush = CreateSolidBrush(random_color())
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def blur(hdc, w, h, offset=4, speed=70):
    """blur effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    mhdc = CreateCompatibleDC(hdc)
    hbit = CreateCompatibleBitmap(hdc, w, h)
    holdbit = SelectObject(mhdc, hbit)
    BitBlt(mhdc, 0, 0, w, h, hdc, 0, 0, win32con.SRCCOPY)
    AlphaBlend(hdc, randint(-offset, offset), randint(-offset, offset), w, h, mhdc, 0, 0, w, h, (0, 0, speed, 0))
    SelectObject(mhdc, holdbit)
    DeleteObject(holdbit)
    DeleteObject(hbit)
    DeleteDC(mhdc)

def radial_blur(hdc, w, h, lp_extra=30, speed=1000):
    """blur + rotate tunnel effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
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

def hatch_brush(hdc, w, h, style: HatchBrushStyle = HatchBrushStyle.RANDOM, set_bk_color=True):
    """inverting random colors + many lines"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    brush = CreateHatchBrush(style.value if style.value != 6 else randint(0, 5), random_color())
    if set_bk_color:
        SetBkColor(hdc, random_color())
    SelectObject(hdc, brush)
    PatBlt(hdc, 0, 0, w, h, win32con.PATINVERT)
    DeleteObject(brush)

def color_filter(hdc, w, h, color):
    """color filter"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    brush = CreateSolidBrush(color)
    SelectObject(hdc, brush)
    BitBlt(hdc, 0, 0, w, h, hdc, 0, 0, win32con.MERGECOPY)
    DeleteObject(brush)

def random_color_filter(hdc, w, h):
    """random color filter"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=qnngjSVvpzM (codeFlane python adaptation)
    clean([w, h])
    brush = CreateSolidBrush(random_color())
    SelectObject(hdc, brush)
    BitBlt(hdc, 0, 0, w, h, hdc, 0, 0, win32con.MERGECOPY)
    DeleteObject(brush)

def tunnel(hdc, w, h, size=60):
    """copy window in small version that makes tunnel effect"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    StretchBlt(hdc, size, size, w - size * 2, h - size * 2, hdc, 0, 0, w, h, win32con.SRCCOPY)

def flip_v(hdc, w, h):
    """flip screen vertically"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    StretchBlt(hdc, 0, h, w, -h, hdc, 0, 0, w, h, win32con.SRCCOPY)

def flip_h(hdc, w, h):
    """flip screen horizontally"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    StretchBlt(hdc, w, 0, -w, h, hdc, 0, 0, w, h, win32con.SRCCOPY)

def draw_icons_on_mouse(hdc, icon=extract(IconSourceDLL.SHELL, 0)):
    """draw icons behind mouse"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    cursor = get_cursor_pos()
    draw(hdc, cursor[0], cursor[1], icon)

def draw_icons_on_clicked_mouse(hdc, button=MouseButton.LEFT, icon=extract(IconSourceDLL.SHELL, ShellIcon.STAR)):
    """draw icons behind mouse (only on click)"""
    #by CYBER SOLDIER https://www.youtube.com/watch?v=bygzc75iw9g (codeFlane python adaptation)
    if is_mouse_pressed(button):
        cursor = get_cursor_pos()
        draw(hdc, cursor[0], cursor[1], icon)