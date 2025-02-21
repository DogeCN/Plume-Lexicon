from subprocess import Popen
from ctypes import WinDLL
import os


Kernel = WinDLL("kernel32")
Shell = WinDLL("shell32")


def GetLanguage():
    if Kernel.GetSystemDefaultUILanguage() == 0x804:
        return 0
    else:
        return 1


def Speak(text: str):
    Popen(f'mshta vbscript:CreateObject("SAPI.SpVoice").Speak("{text}")(window.close)')


def RefreshIcons():
    Shell.SHChangeNotify(0x8000000, 0, 0, 0)


def Explore(path: str):
    if not os.path.exists(path):
        return
    path = path.replace("/", "\\")
    cmd = "select" if os.path.isfile(path) else "e"
    Popen(f'explorer /{cmd},"{path}"')


def GetNewFileName(fn: str, ext: str = "", exclusions: list[str] = []):
    fn = fn + "%s" + ext
    efn = lambda fn: fn in exclusions or os.path.exists(fn)
    if efn(fn % ""):
        i = 2
        while efn(fn % f"({i})"):
            i += 1
        fn = fn % f"({i})"
    else:
        fn = fn % ""
    return fn


def ConvertSize(byte: int):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024
    for u in units:
        _ = byte // size
        if _ < 1:
            return f"{byte}{u}"
        byte = _
    return f"{byte}{units[-1]}"


def CleanDir(path: str):
    total = 0
    for root, dir, files in os.walk(path, topdown=False):
        for name in files:
            try:
                fn = os.path.join(root, name)
                size = os.path.getsize(fn)
                os.remove(fn)
                total += size
            except:
                ...
        for name in dir:
            try:
                os.rmdir(os.path.join(root, name))
            except:
                ...
    return total


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
