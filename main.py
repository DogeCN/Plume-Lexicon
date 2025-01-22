from logic import LMainWindow
from libs.stdout import print, log_init
from libs.debris import Refresh_Icons
from libs.configs.public import Publics
import time, winreg, traceback, warnings, info, line_profiler

warnings.filterwarnings('ignore')

print(f'{info.prog_name} {info.version} By {info.author}', 'Yellow', 'Bold')
print('Starting...\n', 'Green', 'Bold')

def main():
    fr = info.running
    try: difftime = time.time() - info.os.path.getatime(fr)
    except: open(fr, 'w').close()
    else:
        if difftime < 1:
            if info.argv1:  open(fr, 'a').write(f'{info.argv1}\n')
            else: open(fr, 'a').write(f'{info.running_sign}\n')
            return
    log_init()
    LMainWindow()
    info.app.exec()

def register(): #For PyInstaller Exe
    if info.exe:
        sub_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, info.reg_ext)
        winreg.SetValue(sub_key, info.reg_cmd, winreg.REG_SZ, info.cmd)
        Refresh_Icons()
        print('Registered')

if Publics['debug']:
    print('Debug Mode ON', 'Red', 'Bold')
    main()
else:
    register()
    try: main()
    except Exception as e:
        print(f"Error: {''.join(traceback.format_exception(e))}", 'Red', 'Bold')
