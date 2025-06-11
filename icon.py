import os
from win32gui import ExtractIconEx, DrawIcon, DestroyIcon, CreateSolidBrush, FillRect
from enum import Enum
from __init__ import get_hdc

class IconSourceDLL(Enum):
    SHELL = r"C:\Windows\System32\Shell32.dll"
    USER = r"C:\Windows\System32\User32.dll"
    IMAGERES = r"C:\Windows\System32\imageres.dll"

class ShellIcon(Enum):
    """Icons Shell32.dll contains
    Icon tested in Windows 11 system - in windows 10 some icons may has incorrect name
    work in progress
    MADE: 150/452
    #old: icons with low quality
    #{number}: icon that has similar copies with {number} id (may more than 1 copies)
    also comments can contain short description
    """
    FILE = 0
    TEXT_A_FILE = 1 #text file with "A" letter
    EXE_PROGRAM = 2
    FOLDER = 3 #4, 86
    DISK_SAVE_DISK = 5
    DISK_SAVE_DISKETTE = 6
    DISK = 7 #8, 79, 124
    DISK_CABLE = 9 #149
    DISK_CABLE_DISABLED = 10
    DISK_CIRCLE_DISK = 11
    MEMORY = 12
    EARTH = 13
    PC_EARTH = 14 #17,103
    PC = 15
    PRINTER = 16 #136
    CONNECTED_3_PCs = 18
    FOLDER_9_RECTS = 19 #36
    FILE_CLOCK = 20
    CONTROL_PANEL = 21 #57
    MAGNIFYING_GLASS = 22
    QUESTION_MARK = 23
    EXECUTE = 24 #76; Win+R icon
    PC_MOON = 25
    FLASH_DRIVE_ARROW = 26
    SHUT_DOWN = 27
    SMALL_SHARE = 28
    SMALL_ARROW = 29
    SMALL_ARCHIVE = 30
    EMPTY_RECYCLE_BIN = 31 #145
    FULL_RECYCLE_BIN = 32 #62,63,64
    FOLDER_2_PCs = 33 #old
    MONITOR = 34
    FOLDER_TOOLS = 35 #old
    FOLDER_PRINTER = 37 #old
    FOLDER_FONTS = 38 #folder with "A" letter
    SETTINGS_WINDOW = 39 #window with switches buttons
    CIRCLE_DISK_MUSIC = 40 #119
    TREE = 41 #old
    FOLDER_PC = 42 #old
    STAR = 43
    KEY = 44 #old
    FOLDER_TOP_ARROW = 45
    MONITOR_RECYCLE = 46 #old
    LOCK = 47
    PC_WINDOW = 48 #old
    EMPTY = 49 #50,51,52
    DISK_QUESTION = 53
    UNKNOWN_2_FILES = 54
    FILE_MAGNIFYING_GLASS = 55
    PC_MAGNIFYING_GLASS = 56 #old
    PRINTER_FOLDER = 58
    PRINTER_CABLE = 59 #60
    PRINTER_DISKETTE = 61
    FILE_WARNING = 65
    FOLDER_WARNING = 66 #147
    FOLDER_RENAME_PENCIL = 67 #old
    FILE_RIGHT_ARROW = 68
    FILE_GEAR = 69
    TEXT_FILE = 70
    EXECUTION_FILE = 71 #.bat file icon
    FILE_2_GEARS = 72
    FILE_2_A = 73 #74,75; unknown file with 2 "A" letters
    WARNING = 77
    DISK_ARROW_CIRCLE_DISK = 78 #disk with "share" arrow that indicates on circle disk
    REGEDIT = 80 #old
    PRINTER_SUCCESS = 81
    PRINTER_CABLE_SUCCESS = 82
    PRINTER_DISKETTE_SUCCESS = 83
    FOLDER_NESTING = 84 #old
    FOLDER_CABLE = 85
    WINDOW_CHECK_MARK = 87
    PC_CABLE = 88 #148
    DOUBLE_PCs_CABLE = 89
    WINDOW_GEAR = 90 #old
    NOTE_EARTH = 91 #old
    PC_EARTH_OLD = 92 #old
    MONITOR_PROGRAM = 93 #old; monitor with opened program or windows tab
    MONITOR_CLEAN = 94 #old
    WINDOW_TEXT_9_RECTS = 95 #window with text and 9 rects/buttons with images
    WINDOW_9_RECTS = 96 #same as WINDOW_TEXT_9_RECTS, but without text (lines) from left
    CLEAN_WINDOW = 97
    DOUBLE_CLEAN_WINDOWS = 98
    FILE_CLICKED = 99 #100
    RECYCLE_BIN_3D = 101 #102; old
    KEYS = 104
    PRINTING_PRINTER = 105
    PRINTING_PRINTER_SUCCESS = 106
    PRINTING_PRINTER_CABLE_SUCCESS = 107
    PRINTING_PRINTER_CABLE = 108
    BLOCK = 109
    FOLDER_WINDOW_CHECK_MARK = 110
    KEY_2_USERS = 111 #old
    BLUE_SHUT_DOWN = 112 #old
    CIRCLE_DVD_DISK = 113
    FILES = 114 #old
    FILM = 115
    MUSIC_FILE = 116
    CAMERA = 117 #139
    FILM_MUSIC_FILE = 118
    DISK_CREDIT_CARD = 120
    DISK_SAVE_ANOTHER_DISKETTE = 121 #like DISK_SAVE_DISKETTE
    UPLOAD_BLUE_ARROW = 122
    SMALL_UPLOAD_BLUE_ARROW = 123
    ERROR_DISK_SAVE_ANOTHER_DISKETTE = 125
    DOCUMENT = 126 #win11 "My Documents" folder
    IMAGE = 127 #win11 "Pictures" folder
    MUSIC = 128 #win11 "Music" folder
    VIDEO = 129 #win11 "Video" folder
    BUTTERFLY = 130
    CROSS = 131
    DOUBLE_FILES_GREEN_ARROW = 132
    RENAME = 133
    DOUBLE_TEXT_FILES = 134
    EARTH_RED_ARROW = 135
    PLAY = 137 #video player icon (triangle)
    EARTH_MUSIC = 138
    INTERACTIVE_WHITEBOARD = 140
    DRAWING_ON_MONITOR = 141
    EARTH_PICTURE = 142
    PRINTER_PICTURE = 143
    RED_CHECK_MARK = 144
    SHARE_ROTATED = 146
    HOME_3D_STAR = 150

class UserIcon(Enum):
    """Icons User32.dll contains
    #{number}: icon that has similar copies with {number} id (may more than 1 copies)
    """
    EXE_APPLICATION = 0 #5
    WARNING = 1
    QUESTION = 2
    ERROR = 3
    INFO = 4
    ADMIN = 6


def extract(source: IconSourceDLL | str, icon: int | ShellIcon | UserIcon):
    path = source if isinstance(source, str) else source.value
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")

    icons, _ = ExtractIconEx(path, icon if isinstance(icon, int) else icon.value, 1)
    if not icons:
        raise ValueError(f"Icon #{icon} not found in {path}")
    return icons[0]

def draw(hdc, x, y, icon, rect=True, rect_color=0x202020):
    if rect:
        brush = CreateSolidBrush(rect_color)
        FillRect(hdc, (x, y, x + 32, y + 32), brush)

    DrawIcon(hdc, x, y, icon)

draw(get_hdc(), 500, 500, extract(IconSourceDLL.SHELL, 150))