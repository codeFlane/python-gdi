import winreg
from os.path import join, expanduser
from shutil import copy

def registry_startup(path: str, name: str = 'python-gdi script'):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
    winreg.CloseKey(key)

def folder_startup(path: str):
    copy(path, join(expanduser("~"), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'))