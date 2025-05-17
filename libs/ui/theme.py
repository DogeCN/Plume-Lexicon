from ctypes import POINTER, Structure, byref, c_int, pointer, sizeof, windll, wintypes
import info


class ACCENT_POLICY(Structure):
    _fields_ = [
        ("AccentState", wintypes.DWORD),
        ("AccentFlags", wintypes.DWORD),
        ("GradientColor", wintypes.DWORD),
        ("AnimationId", wintypes.DWORD),
    ]


class WINDOW_COMPOSITION_ATTRIBUTES(Structure):
    _fields_ = [
        ("Attribute", wintypes.DWORD),
        ("Data", POINTER(ACCENT_POLICY)),
        ("SizeOfData", wintypes.ULONG),
    ]


class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


def ChangeDWMAttrib(hWnd: int, attrib: int, color) -> None:
    windll.dwmapi.DwmSetWindowAttribute(
        hWnd, attrib, byref(c_int(color)), sizeof(c_int)
    )


def ChangeDWMAccent(hWnd: int, attrib: int, state: int, color=None) -> None:
    accentPolicy = ACCENT_POLICY()

    winCompAttrData = WINDOW_COMPOSITION_ATTRIBUTES()
    winCompAttrData.Attribute = attrib
    winCompAttrData.SizeOfData = sizeof(accentPolicy)
    winCompAttrData.Data = pointer(accentPolicy)

    accentPolicy.AccentState = state
    if color:
        accentPolicy.GradientColor = color

    windll.user32.SetWindowCompositionAttribute(hWnd, pointer(winCompAttrData))


def ExtendFrameIntoClientArea(HWND: int) -> None:
    margins = MARGINS(-1, -1, -1, -1)
    windll.dwmapi.DwmExtendFrameIntoClientArea(HWND, byref(margins))


def DisableFrameIntoClientArea(HWND: int) -> None:
    margins = MARGINS(0, 0, 0, 0)
    windll.dwmapi.DwmExtendFrameIntoClientArea(HWND, byref(margins))


class Theme:
    theme_names = ["Acrylic", "Dark", "Fusion", "Default"]
    main_bg_color = "rgb(43, 43, 43)"
    default_bg_color = "rgb(30, 30, 30)"
    selected_bg_color = "rgb(60, 60, 60)"
    text_color = "rgb(255, 255, 255)"
    border_color = "rgb(90, 90, 90)"
    hover_border_color = "rgb(0, 170, 255)"
    padding = "3px"
    padding_right = "10px"
    acrylic_wins = []
    acrylic = False

    @classmethod
    def AddAcrylic(cls, win):
        if cls.acrylic:
            cls.ApplyAcrylic(win)
        if win not in cls.acrylic_wins:
            cls.acrylic_wins.append(win)

    @classmethod
    def ApplyAcrylic(cls, win=None):
        info.app.setStyle("Windows11")
        cls.main_bg_color = cls.border_color = cls.selected_bg_color = "transparent"
        cls.default_bg_color = "rgba(60, 60, 60, 60)"
        info.app.setStyleSheet(cls.Get())
        aws = [win] if win else cls.acrylic_wins
        for win in aws:
            hWnd = win.winId()
            ChangeDWMAttrib(hWnd, 20, 1)
            ChangeDWMAccent(hWnd, 30, 3, 0x292929)
            ExtendFrameIntoClientArea(hWnd)

    @classmethod
    def DiscardAcrylic(cls):
        info.app.setStyle("Fusion")
        info.app.setStyle("Windows11")
        cls.acrylic = False
        cls.main_bg_color = "rgb(43, 43, 43)"
        cls.default_bg_color = "rgb(30, 30, 30)"
        cls.selected_bg_color = "rgb(60, 60, 60)"
        cls.border_color = "rgb(90, 90, 90)"
        for win in cls.acrylic_wins:
            hWnd = win.winId()
            ChangeDWMAttrib(hWnd, 20, 0)
            ChangeDWMAccent(hWnd, 30, 0)
            DisableFrameIntoClientArea(hWnd)

    @classmethod
    def Set(cls, theme=None):
        info.app.setStyleSheet("")
        if theme in [0, cls.theme_names[0]]:
            cls.acrylic = True
            cls.ApplyAcrylic()
        else:
            cls.DiscardAcrylic()
            if theme in [1, cls.theme_names[1]]:
                info.app.setStyleSheet(cls.Get())
            if theme in [2, cls.theme_names[2]]:
                info.app.setStyle("Fusion")

    @classmethod
    def Get(cls):
        return f"""
            * {{
                background-color: {cls.main_bg_color};
                color: {cls.text_color};
            }}
            QMenuBar, QMenu {{
                border-radius: 5px;
                padding: {cls.padding};
            }}
            QMenuBar::item, QMenu::item {{
                border-radius: 5px;
                padding: {cls.padding} {cls.padding_right};
            }}
            QMenuBar::item:selected, QMenu::item:selected {{
                background-color: {cls.selected_bg_color};
                border-radius: 5px;
            }}
            QMenu {{
                background-color: {cls.default_bg_color};
            }}
            QMenu::item {{
                background-color: {cls.default_bg_color};
            }}
            QPushButton, QToolButton, QLineEdit, QListWidget, QKeySequenceEdit {{
                background-color: {cls.selected_bg_color};
                border: 1px solid {cls.border_color};
                border-radius: 5px;
            }}
            QLineEdit {{
                padding: {cls.padding};
            }}
            QPushButton {{
                min-width: 70px;
            }}
            QPushButton:disabled {{
                color: rgb(150, 150, 150);
            }}
            QPushButton:hover, QToolButton:hover, QLineEdit:hover, QListWidget:hover, QKeySequenceEdit:hover {{
                border: 1px solid {cls.hover_border_color};
            }}
            QToolTip {{
                background-color: {cls.selected_bg_color};
                border: 0px;
            }}
            QSplitter::handle {{
                border: 0px;
            }}
            QMessageBox, QMessageBox QLabel {{
                background-color: {cls.default_bg_color};
                color: {cls.text_color};
            }}
        """
