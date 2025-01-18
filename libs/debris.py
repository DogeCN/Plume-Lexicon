from pywinstyles.py_win_style import (ChangeDWMAccent, ChangeDWMAttrib,
    ExtendFrameIntoClientArea, DisableFrameIntoClientArea)
from ctypes import windll, c_int
import win32clipboard, os, info

def Get_Language():
    dll_h = windll.kernel32
    if dll_h.GetSystemDefaultUILanguage() == 0x804:
        return 0
    else:
        return 1

def Refresh_Icons():
    windll.Shell32.SHChangeNotify(0x8000000, 0, 0, 0)

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

class QSSFactory:
    theme_names = ['Acrylic', 'Dark', 'Fusion', 'Default']
    main_bg_color = 'rgb(43, 43, 43)'
    menu_bg_color = 'rgb(30, 30, 30)'
    selected_bg_color = 'rgb(60, 60, 60)'
    text_color = 'rgb(255, 255, 255)'
    border_color = 'rgb(90, 90, 90)'
    hover_border_color = 'rgb(0, 170, 255)'
    padding = '3px'
    padding_right = '10px'

    @classmethod
    def Set(cls, theme=None):
        info.app.setStyleSheet('')
        if theme in [0, cls.theme_names[0]]:
            info.app.setStyle('Windows11')
            cls.main_bg_color = \
            cls.border_color = \
            cls.selected_bg_color = 'transparent'
            cls.menu_bg_color = 'rgb(60, 60, 60)'
            for win in info.app.allWindows():
                hWnd = win.winId()
                ChangeDWMAttrib(hWnd, 20, c_int(1))
                ChangeDWMAccent(hWnd, 30, 3, 0x292929)
                ExtendFrameIntoClientArea(hWnd)
            info.app.setStyleSheet(cls.Get())
        else:
            info.app.setStyle('Fusion')
            info.app.setStyle('Windows11')
            for win in info.app.allWindows():
                hWnd = win.winId()
                ChangeDWMAttrib(hWnd, 20, c_int(0))
                ChangeDWMAccent(hWnd, 30, 0)
                DisableFrameIntoClientArea(hWnd)
            cls.main_bg_color = 'rgb(43, 43, 43)'
            cls.menu_bg_color = 'rgb(30, 30, 30)'
            cls.selected_bg_color = 'rgb(60, 60, 60)'
            cls.border_color = 'rgb(90, 90, 90)'
            if theme in [1, cls.theme_names[1]]: info.app.setStyleSheet(cls.Get())
            elif theme in [2, cls.theme_names[2]]: info.app.setStyle('Fusion')

    @classmethod
    def Get(cls):
        return f'''
            QMainWindow {{
                background-color: {cls.main_bg_color};
                border-radius: 5px;
            }}
            QMenuBar {{
                background-color: {cls.main_bg_color};
                color: {cls.text_color};
                border-radius: 5px;
                padding: {cls.padding};
            }}
            QMenuBar::item {{
                background-color: {cls.main_bg_color};
                color: {cls.text_color};
                border-radius: 5px;
                padding: {cls.padding} {cls.padding_right};
            }}
            QMenuBar::item:selected {{
                background-color: {cls.selected_bg_color};
                border-radius: 5px;
            }}
            QMenu {{
                background-color: {cls.menu_bg_color};
                color: {cls.text_color};
                border-radius: 5px;
                padding: {cls.padding};
            }}
            QMenu::item {{
                background-color: {cls.menu_bg_color};
                color: {cls.text_color};
                border-radius: 5px;
                padding: {cls.padding} {cls.padding_right};
            }}
            QMenu::item:selected {{
                background-color: {cls.selected_bg_color};
                border-radius: 5px;
            }}
            QStatusBar {{
                background-color: {cls.main_bg_color};
                color: {cls.text_color};
                border-radius: 5px;
            }}
            QPushButton {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
                min-width: 70px;
            }}
            QPushButton:disabled {{
                background-color: {cls.main_bg_color};
                color: {cls.border_color};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {cls.selected_bg_color};
                border-radius: 5px;
                border: 1px solid {cls.hover_border_color};
            }}
            QLineEdit {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
            }}
            QLineEdit:hover {{
                border: 1px solid {cls.hover_border_color};
            }}
            QLabel {{
                color: {cls.text_color};
                border-radius: 5px;
            }}
            QListWidget {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
            }}
            QListWidget:hover {{
                border: 1px solid {cls.hover_border_color};
            }}
            QToolTip {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 0px;
            }}
            QSplitter::handle {{
                border: 0px;
            }}
            QSplitter::handle:horizontal {{
                width: 5px;
            }}
            QToolButton {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
            }}
            QToolButton:hover {{
                background-color: {cls.selected_bg_color};
                border: 1px solid {cls.hover_border_color};
            }}
            QKeySequenceEdit {{
                background-color: {cls.selected_bg_color};
                color: {cls.text_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
            }}
            QKeySequenceEdit:hover {{
                background-color: {cls.selected_bg_color};
                border: 1px solid {cls.hover_border_color};
            }}
        '''
