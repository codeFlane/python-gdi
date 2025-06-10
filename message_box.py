from enum import Enum
import win32con
import win32gui
import win32api
import ctypes
from os.path import exists
from PIL import Image, ImageWin

RESULTS = ['', 'Ok', 'Cancel', 'Abort', 'Retry', 'Ignore', 'Yes', 'No']
class MessageBoxButton(Enum):
    OK = win32con.MB_OK #Ok (true)
    ARI = win32con.MB_ABORTRETRYIGNORE #Abort (false)/Retry (true)/Ignore (none)
    HELP = win32con.MB_HELP #Ok (true)/ Help (none)
    OC = win32con.MB_OKCANCEL #Ok (true)/ Cancel (false)
    RC = win32con.MB_RETRYCANCEL #Retry (true)/ Cancel (false)
    YN = win32con.MB_YESNO #Yes (true)/No (false)
    YNC = win32con.MB_YESNOCANCEL #Yes (true)/No (false)/Cancel (none)

class MessageBoxIcon(Enum):
    ERROR = win32con.MB_ICONERROR
    WARN = win32con.MB_ICONEXCLAMATION
    INFO = win32con.MB_ICONINFORMATION
    QUESTION = win32con.MB_ICONQUESTION
    INVISIBLE = win32con.MB_USERICON


class MessageBox:
    def __init__(self, title: str, content: str, icon: MessageBoxIcon | None = None, button: MessageBoxButton | None = None):
        self.title = title
        self.content = content
        self.icon = icon.value if icon else 0
        self.button = button.value if button else win32con.MB_OK
        self.result = None

    def show(self):
        """show window"""
        self.result = win32gui.MessageBox(0, self.content, self.title, self.button | self.icon)

        if self.result in (6, 4, 1): self.result_bool = True
        elif (self.button in (MessageBoxButton.OC, MessageBoxButton.RC) and self.result == 2) or self.result in (7, 3): self.result_bool = False
        else: self.result_bool = None

        self.result_str = RESULTS[self.result]

    def close(self):
        """close window
        WARNING: title shouldnt duplicate or dialog may not close!
        """
        dialog = win32gui.FindWindow("#32770", self.title)
        win32gui.PostMessage(dialog, win32con.WM_CLOSE, 0, 0)

    @property
    def closed(self):
        """check if window closed
        WARNING: title shouldnt duplicate or property may return wrong answer!
        """
        return bool(win32gui.FindWindow("#32770", self.title))

#WROTE BY CHATGPT
class CustomMessageBox:
    def __init__(self, title, message, image_path=None, icon_path=None, buttons=("OK",)):
        self.title = title
        self.message = message
        self.image_path = image_path
        self.icon_path = icon_path
        self.buttons = buttons
        self.result = None
        self.hInstance = win32api.GetModuleHandle(None)
        self.className = "CustomMsgBoxClass"

        self.margin_top = 6
        self.margin_side = 20
        self.icon_w = 32
        self.icon_h = 32
        self.text_w = 280
        self.text_h = 36
        self.extra_vertical_spacing = 12
        self.button_w = 75
        self.button_h = 23
        self.spacing = 12
        self.btn_area_h = self.button_h + 22
        self.bottom_padding = 20

        lf = win32gui.LOGFONT()
        lf.lfHeight = -12
        lf.lfFaceName = "Segoe UI"
        self.font = win32gui.CreateFontIndirect(lf)

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        elif msg == win32con.WM_COMMAND:
            btn_id = win32api.LOWORD(wparam)
            self.result = self.buttons[btn_id]
            win32gui.DestroyWindow(hwnd)
            return 0
        elif msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            if self.image_path and exists(self.image_path):
                img = Image.open(self.image_path).convert("RGBA").resize((self.icon_w, self.icon_h))
                dib = ImageWin.Dib(img)
                dib.draw(hdc, (
                    self.margin_side,
                    self.margin_top,
                    self.margin_side + self.icon_w,
                    self.margin_top + self.icon_h
                ))
            win32gui.EndPaint(hwnd, ps)
            return 0
        elif msg == win32con.WM_CTLCOLORSTATIC:
            hdc = wparam
            hwnd_static = lparam
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
            if hasattr(self, 'bg_static') and hwnd_static == self.bg_static:
                return win32gui.GetSysColorBrush(win32con.COLOR_3DFACE)
            return win32gui.GetSysColorBrush(win32con.COLOR_WINDOW)
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def show(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.hInstance = self.hInstance
        wc.lpszClassName = self.className
        wc.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wc.hbrBackground = win32gui.GetSysColorBrush(win32con.COLOR_WINDOW)
        try:
            win32gui.RegisterClass(wc)
        except win32gui.error:
            pass

        content_h = max(self.icon_h, self.text_h) + 2 * self.margin_top + self.extra_vertical_spacing
        total_btn_w = len(self.buttons) * self.button_w + (len(self.buttons) - 1) * self.spacing
        win_w = max(self.icon_w + self.text_w + 3 * self.margin_side, total_btn_w + 2 * self.margin_side)
        win_h = content_h + self.btn_area_h + self.bottom_padding + 10

        screen_w = win32api.GetSystemMetrics(0)
        screen_h = win32api.GetSystemMetrics(1)
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2

        hwnd = win32gui.CreateWindowEx(
            0, self.className, self.title,
            win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_VISIBLE,
            x, y, win_w, win_h,
            0, 0, self.hInstance, None
        )
        self.hwnd = hwnd

        if self.icon_path and exists(self.icon_path):
            hicon = win32gui.LoadImage(0, self.icon_path, win32con.IMAGE_ICON,
                                       16, 16, win32con.LR_LOADFROMFILE)
            if hicon:
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)

        # Серый фон кнопок
        self.bg_static = win32gui.CreateWindowEx(
            0, "Static", "",
            win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.SS_NOTIFY,
            0, content_h, win_w, self.btn_area_h + self.bottom_padding,
            hwnd, 0, self.hInstance, None
        )

        # Текст справа от иконки
        text_hwnd = win32gui.CreateWindow(
            "Static", self.message,
            win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.SS_LEFT,
            self.icon_w + 2 * self.margin_side, self.margin_top + 4,
            self.text_w, self.text_h,
            hwnd, 1001, self.hInstance, None
        )
        win32gui.SendMessage(text_hwnd, 0x0030, self.font, True)

        # Кнопки справа
        start_x = win_w - self.margin_side - total_btn_w
        btn_y = content_h + (self.btn_area_h - self.button_h) // 2

        for i, label in enumerate(self.buttons):
            style = win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.BS_PUSHBUTTON
            if i == 0:
                style |= win32con.BS_DEFPUSHBUTTON

            btn_hwnd = win32gui.CreateWindow(
                "Button", label,
                style,
                start_x + i * (self.button_w + self.spacing), btn_y,
                self.button_w, self.button_h,
                hwnd, i, self.hInstance, None
            )
            win32gui.SendMessage(btn_hwnd, 0x0030, self.font, True)
            if i == 0:
                win32gui.SetFocus(btn_hwnd)

        # Показ
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hwnd)
        win32gui.PumpMessages()
        return self.result

    def close(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)