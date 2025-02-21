from libs.io.stdout import print, logInit
from libs.configs.public import Publics
import time, traceback, warnings, info

warnings.filterwarnings("ignore")


fr = info.running
try:
    difftime = time.time() - info.os.path.getatime(fr)
except:
    open(fr, "w").close()
else:
    if difftime < 1:
        if info.argv1:
            open(fr, "a").write(f"{info.argv1}\n")
        else:
            open(fr, "a").write(f"{info.running_sign}\n")
        info.sys.exit()


def main():
    print(f"{info.prog_name} {info.version} By {info.author}", "Yellow", "Bold")
    print("Starting...\n", "Green", "Bold")
    from logic import LMainWindow

    LMainWindow()
    info.app.exec()


if Publics["debug"]:
    print("Debug Mode ON", "Red", "Bold")
    main()
else:
    logInit()
    try:
        main()
    except Exception as e:
        print(f"Error: {''.join(traceback.format_exception(e))}", "Red", "Bold")
