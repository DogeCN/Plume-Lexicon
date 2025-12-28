from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal, QObject
from libs.configs import Setting
from libs.io.stdout import print
from libs.io.requests import get
from libs.io.thread import Worker, Pool
from .db import *
import info


class LSignal(QObject):
    update = Signal()


class CSignal(QObject):
    sre = Signal(bool)
    warn = Signal(str)
    update = Signal()

    def __init__(self):
        super().__init__()
        self.count = 0
        self.locked = False

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


class Lexicon:

    def __init__(self, fp: str):
        self.fp = fp
        self.enabled = self.loaded = self.failed = False
        self.signal = LSignal()
        self.reader = Reader(fp, info.temp_dir + self.filename)
        self.name, self.name_zh = self.reader.name, self.reader.name_zh

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
    def filename(self):
        return self.fp.split("\\")[-1].strip(info.ext_disabled)

    def filter(self, word: str) -> list[str]:
        return self.reader.filter(word, info.seps)

    def __getitem__(self, key: str):
        return self.reader[key]

    def __len__(self) -> int:
        return len(self.reader)

    def __contains__(self, key: str) -> bool:
        return key in self.reader

    def setEnabled(self, e):
        if e and not self.loaded:
            csignal.begin()
            try:
                self.reader.load()
                matcher.combine(self.reader)
                self.loaded = True
                self.failed = False
            except Exception as ex:
                print(f'Failed to load "{self.fp}": {ex}', "Red")
                self.failed = True
            csignal.final()
        self.reader.set_enabled(e)
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
                print(f'Failed to rename "{self.fp}" to "{fp}"', "Red")
            self.fp = fp


class LexiBox(QCheckBox):
    def __init__(self, parent, lexicon: Lexicon):
        super().__init__(parent)
        lexicon.signal.update.connect(self.update)
        self.toggled.connect(lambda e: Worker(lexicon.setEnabled, e))
        self.lexicon = lexicon
        self.update()

    def update(self):
        self.setText(self.lexicon.text)
        self.setChecked(self.lexicon.enabled)
        if self.lexicon.failed:
            self.setStyleSheet(info.StlSheets["red"])
        elif self.lexicon.loaded:
            self.setStyleSheet(info.StlSheets["green"])
        else:
            self.setStyleSheet("")


lexicons: list[Lexicon] = []
matcher = Matcher()


def initLexis(fp, e):
    try:
        l = Lexicon(fp)
        Worker(l.setEnabled, e)
        lexicons.append(l)
        csignal.update.emit()
    except OSError as e:
        print(f'Failed to initialize reader for "{fp}": {e}', "Red")


def getLexis(ln):
    name = ln + info.ext_lexi
    print(f"Downloading {name}", "Black")
    for url in (info.ghproxy % info.lurl, info.lurl):
        data = get(url % name)
        if data:
            fp = info.lexis_dir + name
            open(fp, "wb").write(data)
            return initLexis(fp, True)
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
        Worker(downLexis)
