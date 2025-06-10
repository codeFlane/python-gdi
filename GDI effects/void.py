import win32gui
import win32con
import ctypes
import random
import time


hdc = win32gui.GetDC(0)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


x = y = 0
while True:
    hdc = win32gui.GetDC(0)
    win32gui.BitBlt(
        hdc,
        random.randint(1, 10) % 2,
        random.randint(1, 10) % 2,
        w,
        h,
        hdc,
        random.randint(1, 1000) % 2,
        random.randint(1, 1000) % 2,
        win32con.SRCAND,
    )
    time.sleep(0.01)
    win32gui.ReleaseDC(0, hdc)
