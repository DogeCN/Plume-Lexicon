from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal, QObject
from libs.configs.settings import Setting
from libs.stdout import print
from libs.io.base import *
from threading import Thread
from requests import get
import info

class LSignal(QObject):
    update = Signal()

class CSignal(QObject):
    sre = Signal(bool)
    count = 0
    locked = False

    def add(self):
        self.count += 1
        if self.count == 1 and not self.locked:
            self.sre.emit(False)

    def sub(self):
        self.count -= 1
        if not self.count and not self.locked:
            self.sre.emit(True)
    
    def lock(self):
        self.locked = True
        self.sre.emit(False)
    
    def unlock(self):
        self.locked = False
        if not self.count: self.sre.emit(True)

csignal = CSignal()

class Lexicon(dict[str, list[str, list[str]]]):
    name = ''
    name_zh = ''

    def __init__(self, fp:str=None):
        if fp:
            self.fp = fp
            self.enabled = \
            self.loaded = \
            self.failed = False
            self.signal = LSignal()
            if self.hash_exists: self._update(load_(self.hash_file))
            else: self.name = self.name_zh = fp.split('\\')[-1].strip(info.ext_disabled)
    
    @property
    def text(self):
        name = self.name if Setting.Language else self.name_zh
        if self.loaded: hint = len(self)
        elif self.failed: hint = Setting.getTr('loadfailed')
        else: hint = Setting.getTr('unload')
        return f"{name} ({hint})"

    @property
    def hash_file(self):
        return hash_(self.fp.strip(info.ext_disabled).encode())
    
    @property
    def hash_exists(self):
        return info.os.path.exists(self.hash_file)

    def setEnabled(self, enable):
        Thread(target=self._setEnabled, name=self.name, args=(enable,)).start()

    def _setEnabled(self, enable):
        if enable and not self.loaded:
            csignal.add()
            try:
                self._update(load(self.fp))
                if not self.hash_exists:
                    header = Lexicon()
                    header.name = self.name
                    header.name_zh = self.name_zh
                    dump_(self.hash_file, header)
                self.loaded = True
                self.failed = False
            except Exception as e:
                print(f'Failed to load {self.fp}: {e}', 'Red')
                self.failed = True
            csignal.sub()
        self.enabled = enable
        self.signal.update.emit()
        if self.failed: return
        fp = self.fp.strip(info.ext_disabled)
        if not enable:
            fp = fp + info.ext_disabled
        if self.fp != fp:
            info.os.rename(self.fp, fp)
            self.fp = fp

    def _update(self, l):
        self.name = getattr(l, 'name')
        self.name_zh = getattr(l, 'name_zh')
        self.update(l)

class LexiBox(QCheckBox):
    def __init__(self, lexicon:Lexicon, parent):
        super().__init__(parent)
        lexicon.signal.update.connect(self.update)
        self.toggled.connect(lexicon.setEnabled)
        self.lexicon = lexicon
        self.update()
    
    def update(self):
        super().setText(self.lexicon.text)
        self.setChecked(self.lexicon.enabled)
        if self.lexicon.failed: self.setStyleSheet(info.StlSheets['red'])
        elif self.lexicon.loaded: self.setStyleSheet(info.StlSheets['green'])
        else: self.setStyleSheet('')

lexicons = [] #type: list[Lexicon]

def getfile(name, dir):
    try: request = get(info.lurl_cn % name, stream=True, timeout=info.timeout)
    except: request = get(info.lurl % name, stream=True, timeout=info.timeout)
    with open(dir + name, 'wb') as f:
        print(f'Downloading {name}', 'Blue')
        for chunk in request:
            f.write(chunk)

def _load_lexis():
    files = info.os.listdir(info.lexis_dir)
    lexicons.clear()
    for f in files:
        enabled = f.endswith(info.ext_lexi)
        disabled = f.endswith(info.ext_lexi + info.ext_disabled)
        if enabled or disabled:
            fp = info.lexis_dir + f
            lexicon = Lexicon(fp)
            lexicon.setEnabled(enabled)
            lexicons.append(lexicon)
    if not lexicons: return True

def load_lexis(callback):
    if _load_lexis():
        csignal.lock()
        dlpool = [Thread(target=getfile, name=ln,
                    args=(ln + info.ext_lexi,info.lexis_dir)
                    ) for ln in info.default_lexis]
        for t in dlpool: t.start()
        for t in dlpool: t.join()
        csignal.unlock()
        if _load_lexis():
            callback()
