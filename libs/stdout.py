import time, info

stdout = info.sys.stdout
log = info.log


def log_init():
    if not stdout:
        open(log, "w").close()


Attr = {
    "Reset": 0,
    "Bold": 1,
    "Underline": 4,
    "Blink": 5,
    "Reverse": 7,
    "Hidden": 8,
    "Black": 30,
    "Red": 31,
    "Green": 32,
    "Yellow": 33,
    "Blue": 34,
    "Purple": 35,
    "Cyan": 36,
    "White": 37,
}

_getstamp = lambda f: time.strftime(f, time.localtime())


# Redefine the print function
def print(rstr, *attr):
    rstr = str(rstr)
    if "\n" in rstr:
        for r in rstr.split("\n"):
            print(r, *attr)
    else:
        fstr = "\033[%sm"
        attr = ";".join([str(Attr[a]) for a in attr])
        if stdout:
            stdout.write(f"{fstr%attr}{rstr}{fstr%Attr['Reset']}\n")
        else:
            open(log, "a", encoding="utf-8").write(
                f"{_getstamp('[%H:%M:%S]')} {rstr}\n"
            )
