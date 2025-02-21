from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal, QObject
from libs.configs.settings import Setting
from libs.io.base import load, hash, load_, dump_
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
            if self.hashExists:
                self.update(load_(self.hashFile))
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
    def hashFile(self):
        return hash(self.fp.strip(info.ext_disabled).encode())

    @property
    def hashExists(self):
        return info.os.path.exists(self.hashFile)

    def setEnabled(self, e):
        if e and not self.loaded:
            csignal.begin()
            try:
                self.update(load(self.fp))
                if not self.hashExists:
                    header = Lexicon()
                    header.name = self.name
                    header.name_zh = self.name_zh
                    dump_(self.hashFile, header)
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

    def update(self, l):
        self.name = getattr(l, "name")
        self.name_zh = getattr(l, "name_zh")
        super().update(l)


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


def initLexis(fp, e):
    l = Lexicon(fp)
    Thread(l.setEnabled, e)
    lexicons.append(l)
    csignal.update.emit()


def getLexis(ln):
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
        initLexis(fp, True)
    else:
        return ln


def downLexis():
    csignal.lock()
    pool = Pool()
    for ln in info.default_lexis:
        pool.submit(getLexis, ln)
    failed = [ln for ln in pool.wait() if ln]
    csignal.unlock()
    if lexicons:
        if failed:
            csignal.warn.emit(Setting.getTr("down_failed") % ", ".join(failed))
    else:
        csignal.warn.emit(Setting.getTr("lexi_unavailable"))


def loadLexis():
    files = info.os.listdir(info.lexis_dir)
    lexicons.clear()
    csignal.update.emit()
    for f in files:
        enabled = f.endswith(info.ext_lexi)
        disabled = f.endswith(info.ext_lexi + info.ext_disabled)
        if enabled or disabled:
            fp = info.lexis_dir + f
            initLexis(fp, enabled)
    if not lexicons:
        Thread(downLexis)
