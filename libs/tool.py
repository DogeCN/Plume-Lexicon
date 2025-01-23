import os, importlib
from libs.stdout import print
from tools.base import Tool
import info
from tools import one


def load():
    global Tools
    try:
        Tools = dynamic_get()
    except:
        Tools = static_get()


def dynamic_get() -> list[Tool]:
    Tools = []
    dpath = os.path.join(os.getcwd(), info.tools)
    for f in os.listdir(dpath):
        mname = os.path.splitext(f)[0]
        mpath = f"{info.tools}.{mname}"
        module = importlib.import_module(mpath)
        try:
            tool = getattr(module, "tool")
        except AttributeError:
            continue
        Tools.append(tool)
    print(f"Loaded tools: {', '.join(Tools)}", "Bold")
    return Tools


def static_get():
    from tools import batch, convert, random

    return {batch.tool, random.tool, convert.tool, one.tool}


load()
