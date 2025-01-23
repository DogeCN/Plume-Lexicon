from PySide6.QtWidgets import QFileDialog as QFile
from libs.configs.public import Publics


def rdir(f):
    if f:
        rd = f[0] if isinstance(f, list) else f
        rd = "/".join(rd.split("/")[0:-1]) + "/"
        Publics["default_path"] = rd
    return f


class Dialog:

    def OpenDir(parent=None, title="", dir=None) -> str:
        if not dir:
            dir = Publics["default_path"]
        d = QFile.getExistingDirectory(parent, title, dir)
        return rdir(d)

    def OpenFile(parent=None, title="", type=..., dir=None) -> str:
        if not dir:
            dir = Publics["default_path"]
        f, _ = QFile.getOpenFileName(parent, title, dir, type)
        return rdir(f)

    def OpenFiles(parent=None, title=None, type=..., dir=None) -> list[str]:
        if not dir:
            dir = Publics["default_path"]
        f, _ = QFile.getOpenFileNames(parent, title, dir, type)
        return rdir(f)

    def SaveFile(parent=None, title="", type=..., dir=None) -> str:
        if not dir:
            dir = Publics["default_path"]
        f, _ = QFile.getSaveFileName(parent, title, dir, type)
        return rdir(f)
