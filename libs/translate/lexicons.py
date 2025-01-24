from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal, QObject
from libs.configs.settings import Setting
from libs.io.base import *
from libs.io.stdout import print
from libs.io.requests import get
from libs.io.thread import Thread, Pool
import info


class LSignal(QObject):
    update = Signal()


class CSignal(QObject):
    sre = Signal(bool)
    warn = Signal(str)
    update = Signal()
    count = 0
    locked = False

    def begin(self):
        self.count += 1
        if self.count == 1 and not self.locked:
            self.sre.emit(False)

    def final(self):
        self.count -= 1
        if not self.count and not self.locked:
            self.sre.emit(True)

    def lock(self):
        self.locked = True
        self.sre.emit(False)

    def unlock(self):
        self.locked = False
        if not self.count:
            self.sre.emit(True)


csignal = CSignal()


class Lexicon(dict[str, list[str, list[str]]]):
    name = ""
    name_zh = ""

    def __init__(self, fp: str = None):
        if fp:
            self.fp = fp
            self.enabled = self.loaded = self.failed = False
            self.signal = LSignal()
            if self.hash_exists:
                self._update(load_(self.hash_file))
            else:
                self.name = self.name_zh = fp.split("\\")[-1].strip(info.ext_disabled)

    @property
    def text(self):
        name = self.name if Setting.Language else self.name_zh
        if self.loaded:
            hint = len(self)
        elif self.failed:
            hint = Setting.getTr("load_failed")
        else:
            hint = Setting.getTr("unload")
        return f"{name} ({hint})"

    @property
    def hash_file(self):
        return hash_(self.fp.strip(info.ext_disabled).encode())

    @property
    def hash_exists(self):
        return info.os.path.exists(self.hash_file)

    def setEnabled(self, e):
        if e and not self.loaded:
            csignal.begin()
            try:
                self._update(load(self.fp))
                if not self.hash_exists:
                    header = Lexicon()
                    header.name = self.name
                    header.name_zh = self.name_zh
                    dump_(self.hash_file, header)
                self.loaded = True
                self.failed = False
            except Exception as ex:
                print(f"Failed to load {self.fp}: {ex}", "Red")
                self.failed = True
            csignal.final()
        self.enabled = e
        self.signal.update.emit()
        if self.failed:
            return
        fp = self.fp.strip(info.ext_disabled)
        if not e:
            fp = fp + info.ext_disabled
        if self.fp != fp:
            try:
                info.os.rename(self.fp, fp)
            except OSError:
                print(f"Failed to rename {self.fp} to {fp}", "Red")
            self.fp = fp

    def _update(self, l):
        self.name = getattr(l, "name")
        self.name_zh = getattr(l, "name_zh")
        self.update(l)


class LexiBox(QCheckBox):
    def __init__(self, parent, lexicon: Lexicon):
        super().__init__(parent)
        lexicon.signal.update.connect(self.update)
        self.toggled.connect(lambda e: Thread(lexicon.setEnabled, e))
        self.lexicon = lexicon
        self.update()

    def update(self):
        super().setText(self.lexicon.text)
        self.setChecked(self.lexicon.enabled)
        if self.lexicon.failed:
            self.setStyleSheet(info.StlSheets["red"])
        elif self.lexicon.loaded:
            self.setStyleSheet(info.StlSheets["green"])
        else:
            self.setStyleSheet("")


lexicons = []  # type: list[Lexicon]


def init_lexis(fp, e):
    l = Lexicon(fp)
    Thread(l.setEnabled, e)
    lexicons.append(l)
    csignal.update.emit()


def get_lexis(ln):
    data = None
    name = ln + info.ext_lexi
    print(f"Downloading {name}", "Black")
    for url in (info.lurl_cn, info.lurl):
        try:
            data = get(url % name)
        except:
            continue
    if data:
        fp = info.lexis_dir + name
        open(fp, "wb").write(data)
        init_lexis(fp, True)
    else:
        return ln


def down_lexis():
    csignal.lock()
    pool = Pool()
    for ln in info.default_lexis:
        pool.submit(get_lexis, ln)
    failed = pool.wait()
    csignal.unlock()
    if lexicons:
        csignal.warn.emit(
            Setting.getTr("down_failed") % ", ".join(ln for ln in failed if ln)
        )
    else:
        csignal.warn.emit(Setting.getTr("lexi_unavailable"))


def load_lexis():
    files = info.os.listdir(info.lexis_dir)
    lexicons.clear()
    csignal.update.emit()
    for f in files:
        enabled = f.endswith(info.ext_lexi)
        disabled = f.endswith(info.ext_lexi + info.ext_disabled)
        if enabled or disabled:
            fp = info.lexis_dir + f
            init_lexis(fp, enabled)
    if not lexicons:
        Thread(down_lexis)
