import ctypes
import win32con
#https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)