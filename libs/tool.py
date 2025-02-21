from libs.io.stdout import print
from tools.base import Tool
import importlib, info


def load():
    global Tools
    try:
        Tools = dynamicGet()
    except:
        Tools = staticGet()


def dynamicGet() -> list[Tool]:
    Tools = []
    names = []
    dpath = info.os.path.join(info.os.getcwd(), info.tools)
    for f in info.os.listdir(dpath):
        if f.startswith("_"):
            continue
        mname = info.os.path.splitext(f)[0]
        names.append(mname)
        mpath = f"{info.tools}.{mname}"
        module = importlib.import_module(mpath)
        try:
            tool = getattr(module, "tool")
        except AttributeError:
            continue
        Tools.append(tool)
    print(f"Loaded tools: {', '.join(names)}", "Bold")
    return Tools


def staticGet():
    from tools import batch, random, convert, one

    return {batch.tool, random.tool, convert.tool, one.tool}


load()
