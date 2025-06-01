from ctypes import WinDLL


Kernel = WinDLL("kernel32")
Shell = WinDLL("shell32")
Dwm = WinDLL("dwmapi")
User = WinDLL("user32")
