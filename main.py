from PySide6.QtWidgets import QApplication
import sys, time, winreg, traceback
from logic import LMainWindow
from libs.stdout import print, log_init
from libs.debris import Refresh_Icons
import info

print(f'{info.prog_name} {info.version} By {info.author}', 'Yellow', 'Bold')
print('Starting...\n', 'Green', 'Bold')

def main():
    argv = sys.argv[1] if len(sys.argv) > 1 else None
    fr = info.running
    try: difftime = time.time() - info.os.path.getatime(fr)
    except: open(fr, 'w').close()
    else:
        if difftime < 1:
            if argv:  open(fr, 'a').write(f'{argv}\n')
            else: open(fr, 'a').write(f'{info.running_sign}\n')
            return
    log_init()
    app = QApplication()
    LMainWindow(argv)
    app.exec()

def register(): #For PyInstaller Exe
    file = sys.argv[0]
    if file.endswith(info.ext_self_exe):
        sub_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, info.reg_ext)
        winreg.SetValue(sub_key, info.reg_cmd, winreg.REG_SZ, f'"{file}" "%1"')
        Refresh_Icons()
        print('Registered')

if info.debug:
    print('Debug Mode ON', 'Red', 'Bold')
    main()
else:
    register()
    try: main()
    except Exception as e:
        print(f"Error: {''.join(traceback.format_exception(e))}", 'Red', 'Bold')
