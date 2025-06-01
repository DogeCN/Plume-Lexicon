from libs.windll import Kernel, Shell
from itertools import count
from subprocess import Popen
import os, winreg


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
