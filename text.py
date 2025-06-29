from win32gui import *

def create_font(font, height=14):
    lf = LOGFONT()
    lf.lfHeight = -height
    lf.lfFaceName = font
    return CreateFontIndirect(lf)
#SOON