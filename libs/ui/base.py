from ctypes import POINTER, Structure, byref, c_int, pointer, sizeof, windll, wintypes

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
    windll.dwmapi.DwmSetWindowAttribute(hWnd, attrib, byref(c_int(color)), sizeof(c_int))

def ChangeDWMAccent(hWnd: int, attrib: int, state: int, color = None) -> None:
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
