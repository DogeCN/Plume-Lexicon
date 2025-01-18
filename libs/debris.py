from PySide6.QtWidgets import QMainWindow
from pywinstyles import apply_style
import win32clipboard, platform, ctypes, os

def Set_Acrylic(window:QMainWindow):
    try:
        assert int(platform.release()) > 10
        #apply_style(window, 'acrylic')
    except: ...

def Get_Language():
    dll_h = ctypes.windll.kernel32
    if dll_h.GetSystemDefaultUILanguage() == 0x804:
        return 0
    else:
        return 1

def Refresh_Icons():
    ctypes.windll.Shell32.SHChangeNotify(0x8000000, 0, 0, 0)

def Get_New_File_Name(fn:str, ext:str='', exclusions:list[str]=[]):
    fn = fn + '%s' + ext
    efn = lambda fn:fn in exclusions or os.path.exists(fn)
    if efn(fn%''):
        i = 2
        while efn(fn%f'({i})'):
            i += 1
        fn = fn%f'({i})'
    else: fn = fn%''
    return fn

def Convert_Size(byte:int):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    size = 1024
    for u in units:
        _ = byte // size
        if _ < 1:
            return f'{byte}{u}'
        byte = _
    return f'{byte}{units[-1]}'

def Clean_Dir(path:str):
    total = 0
    for root, dir, files in os.walk(path, topdown=False):
        for name in files:
            try:
                fn = os.path.join(root, name)
                size = os.path.getsize(fn)
                os.remove(fn)
                total += size
            except: ...
        for name in dir:
            try: os.rmdir(os.path.join(root, name))
            except: ...
    return total

class Clipboard:
    
    def Write(text:str):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
    
    def Read():
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return text

class Ticker:
    tick = 0

    def __init__(self, interval=20):
        self.interval = interval

    def __bool__(self):
        if self.tick >= self.interval:
            self.tick = 0
            return True
        else:
            self.tick += 1
            return False
