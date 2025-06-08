from ctypes import POINTER, Structure, wintypes, byref, c_int, pointer, sizeof, WinDLL
from itertools import count
from subprocess import Popen
import os, winreg


Kernel = WinDLL("kernel32")
Shell = WinDLL("shell32")
Dwm = WinDLL("dwmapi")
User = WinDLL("user32")


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


class HWND(int):

    def ChangeDWMAttrib(self, attrib: int, color) -> None:
        Dwm.DwmSetWindowAttribute(self, attrib, byref(c_int(color)), sizeof(c_int))

    def ChangeDWMAccent(self, attrib: int, state: int, color=None) -> None:
        accentPolicy = ACCENT_POLICY()

        winCompAttrData = WINDOW_COMPOSITION_ATTRIBUTES()
        winCompAttrData.Attribute = attrib
        winCompAttrData.SizeOfData = sizeof(accentPolicy)
        winCompAttrData.Data = pointer(accentPolicy)

        accentPolicy.AccentState = state
        if color:
            accentPolicy.GradientColor = color

        User.SetWindowCompositionAttribute(self, pointer(winCompAttrData))

    def ExtendFrameIntoClientArea(self) -> None:
        margins = MARGINS(-1, -1, -1, -1)
        Dwm.DwmExtendFrameIntoClientArea(self, byref(margins))

    def DisableFrameIntoClientArea(self) -> None:
        margins = MARGINS(0, 0, 0, 0)
        Dwm.DwmExtendFrameIntoClientArea(self, byref(margins))


def GetLanguage():
    if Kernel.GetSystemDefaultUILanguage() == 0x804:
        return 0
    else:
        return 1


def Speak(text: str):
    Popen(f'mshta vbscript:CreateObject("SAPI.SpVoice").Speak("{text}")(window.close)')


def RefreshIcons():
    Shell.SHChangeNotify(0x8000000, 0, 0, 0)


def Register(ext: str, command: str):
    SubKey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\" + ext)
    winreg.SetValue(SubKey, "shell\\open\\command", winreg.REG_SZ, command)
    RefreshIcons()


def Explore(path: str):
    if os.path.exists(path):
        path = path.replace("/", "\\")
        cmd = "select" if os.path.isfile(path) else "e"
        Popen(f'explorer /{cmd},"{path}"')


def GetNewFileName(fn: str, ext: str = "", exclusions: list[str] = []):
    base = f"{fn}{ext}"
    if base not in exclusions:
        return base
    for i in count(2):
        candidate = f"{fn}({i}){ext}"
        if candidate not in exclusions:
            return candidate


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
