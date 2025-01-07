from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal, QObject
from concurrent.futures import ThreadPoolExecutor
from requests import get
from libs.io.base import _dump, _load, load, _hash
from libs.configs.settings import Setting
from libs.stdout import print
import info

pool = ThreadPoolExecutor(3)

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
    
    def __init__(self, fn:str=None):
        self.fn = fn
        if fn:
            self.enabled = \
            self.loaded = \
            self.failed = False
            self.signal = LSignal()
            if self.hash_exists: self._update(_load(self.hash_file))
            else: self.name = self.name_zh = fn.split('\\')[-1].strip(info.ext_disabled)
    
    @property
    def text(self):
        name = self.name if Setting.Language else self.name_zh
        if self.loaded: hint = len(self)
        elif self.failed: hint = Setting.getTr('loadfailed')
        else: hint = Setting.getTr('unload')
        return f"{name} ({hint})"

    @property
    def hash_file(self):
        return _hash(self.fn.strip(info.ext_disabled).encode())
    
    @property
    def hash_exists(self):
        return info.os.path.exists(self.hash_file)

    def setEnabled(self, enable):
        pool.submit(self._setEnabled, enable)

    def _setEnabled(self, enable):
        csignal.add()
        if enable and not self.loaded:
            try:
                self._update(load(self.fn))
                if not self.hash_exists:
                    header = Lexicon()
                    header.name = self.name
                    header.name_zh = self.name_zh
                    _dump(self.hash_file, header)
                self.loaded = self.enabled = True
                self.failed = False
                self.signal.update.emit()
            except:
                self.failed = True
                self.signal.update.emit()
                csignal.sub()
                return
        fn = self.fn.strip(info.ext_disabled)
        if not enable:
            fn = fn + info.ext_disabled
            self.enabled = False
        if self.fn != fn:
            info.os.rename(self.fn, fn)
            self.fn = fn
        csignal.sub()

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
            fn = info.lexis_dir + f
            lexicon = Lexicon(fn)
            lexicon.setEnabled(enabled)
            lexicons.append(lexicon)
    if not lexicons: return True

def load_lexis(callback):
    if _load_lexis():
        dlpool = ThreadPoolExecutor()
        csignal.lock()
        for lname in info.default_lexis:
            fname = lname + info.ext_lexi
            dlpool.submit(getfile, fname, info.lexis_dir)
        dlpool.shutdown()
        csignal.unlock()
        if _load_lexis():
            callback()
