from PySide6.QtWidgets import QMessageBox, QMainWindow
from PySide6.QtCore import Signal, QObject
from libs.translate.dict import load_lexis
from libs.ui.main import Ui_MainWindow
from libs.ui.main.base import FItem
from libs.debris import Clipboard, Ticker
from libs.translate import Result
from libs.config import Setting
from libs.public import Publics
from libs.io import dialog
from win32com.client import Dispatch
from threading import Thread
from requests import get
from time import sleep
import webbrowser, info

class LSignal(QObject):
    set_result_singal = Signal()
    callback_singal = Signal()
    show_lexis_singal = Signal()
    show_update_singal = Signal(dict)
    exchange_singal = Signal(Result)
    expand_singal = Signal(Result)
    def __init__(self):
        super().__init__()

class LMain(Ui_MainWindow):
    _voice = Dispatch('SAPI.SpVoice')
    _result = Result()
    signal = LSignal()
    lexi_thread = Thread()
    add_locked = False
    add_enabled = True
    exchanges = None
    expands = None
    parent = None
    raw = None
    tc = False
    hc = False

    def set_add_enabled(self, e):
        self.add_enabled = e
        self.Add.setEnabled(False if self.add_locked else e)
    def set_add_locked(self, l):
        self.add_locked = l
        self.Add.setEnabled(False if l else self.add_enabled)
    def load_lexis(self):
        self.lexi_thread = Thread(target=self._load_lexis)
        self.lexi_thread.start()
    def _load_lexis(self):
        load_lexis(self.signal.callback_singal.emit)
        self.signal.show_lexis_singal.emit()
    def save_all(self, silent=True):
        for item in self.Files.items: item.save(silent)
    def check(self): self.set_add_locked(not len(self.Files.items))
    def append(self, result): self.Bank.append(result); self.Files.keep()
    def close(self): info.prog_running = False; self.parent.close()
    def clear(self): self.Bank.clear(); self.Files.keep()
    def top(self): self.Bank.top(); self.Files.keep()
    def set_expand(self, results): self.Expand.results = results
    def set_exchanges(self, results): self.Exchanges.results = results

    def __init__(self, MainWindow:QMainWindow):
        super().__init__()
        self.setupUi(MainWindow)
        self.parent = MainWindow
        self.raw = QMainWindow(MainWindow)
        self.raw.setStyleSheet(info.StlSheets['raw'])
        if not info.debug:
            Thread(target=self.check_update).start()
        Thread(target=self.handle).start()
        self.connect_actions()
    
    def connect_actions(self):
        #Menu Actions
        self.actionNew.triggered.connect(lambda:self.Files.new() and self.check())
        self.actionReload.triggered.connect(lambda:(lambda item:item.load() or self._display_file(item) if item else self.load())(self.Files.current) or self.check())
        self.actionLoad.triggered.connect(lambda:(lambda f:self._display_file(self.Files.load(f)[0]) if f else ...)(dialog.OpenFiles(self.parent, Setting.getTr('load'), info.ext_all_voca)) or self.check())
        self.actionSave.triggered.connect(lambda:self.Files.current.save())
        self.actionSave_All.triggered.connect(lambda:self.save_all(False))
        self.actionSave_As.triggered.connect(lambda:self.Files.current.save_as())
        self.actionRemove.triggered.connect(lambda:self.Files.remove() or self.check())
        self.actionClear.triggered.connect(lambda:self.Files.clear() or self.check())
        self.actionExit.triggered.connect(self.close)
        self.actionCheck.triggered.connect(lambda:Thread(target=self.check_update).start())
        self.actionAbout.triggered.connect(lambda:webbrowser.open(info.repo_url))
        self.actionAboutQt.triggered.connect(lambda:QMessageBox.aboutQt(self.raw))
        #Button Actions
        self.Add.clicked.connect(self.command_add)
        self.Delete.clicked.connect(self.Bank.remove)
        self.Top.clicked.connect(self.top)
        #Text
        self.Word_Entry.textChanged.connect(self.text_change)
        self.Translated_text.mouseDoubleClickEvent = self.correct
        self.Phonetic.mouseDoubleClickEvent = lambda *evt:Thread(target=lambda:self._voice.Speak(self.Word_Entry.text()) if self.result else ..., daemon=True).start()
        #List Widgets
        self.Files.itemSelectionChanged.connect(self.display_file)
        self.Bank.itemSelectionChanged.connect(self.display_selection)
        self.Exchanges.itemSelectionChanged.connect(self.display_exchanges)
        self.Expand.itemSelectionChanged.connect(self.display_phrases)
        #Signal
        self.signal.set_result_singal.connect(self.set_result)
        self.signal.show_update_singal.connect(self.show_update)
        self.signal.callback_singal.connect(lambda:QMessageBox.warning(self.raw, Setting.getTr('warning'), Setting.getTr('translate_function_unavailable')))
        self.signal.exchange_singal.connect(lambda r: self.set_exchanges(r) if not self.tc else ...)
        self.signal.expand_singal.connect(lambda r: self.set_expand(r) if not self.tc else ...)

    def setShotcuts(self):
        self.Add.setShortcut(Setting.Key_Add)
        self.Delete.setShortcut(Setting.Key_Del)
        self.Top.setShortcut(Setting.Key_Top)

    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, result:Result):
        self._result = result
        word = result.word
        self.Translated_text.setText(result.get_translation())
        self.Translated_text.setToolTip(result.get_definition())
        self.Phonetic.setText(result.phonetic)
        if word in self.Bank.words or not result:
            self.set_add_enabled(False)
        else:
            self.set_add_enabled(True)

    def correct(self, *evt):
        result = self.result
        if result.match:
            self.Word_Entry.setText(result.word)
            result.match = False
        elif result:
            Clipboard.Write(result.get_translation())

    def set_result(self):
        result = self.result
        if result.match:
            self.Translated_text.setText(result.get_tip())
            self.Translated_text.setToolTip(Setting.getTr('correct_hint'))
        elif result:
            self.Phonetic.setToolTip(info.speech_hint % Setting.getTr('speech_hint'))
            self.hc = True
            self.exchanges = result.exchanges
            self.expands = result.expands
            self.result = result

    def _handle(self, generator, emit):
        if generator:
            results = []
            for r in generator:
                results.append(r)
                if self.hc:
                    self.hc = False
                    return True
            emit(results)

    def handle(self):
        ticker = Ticker()
        while info.prog_running:
            if self.parent.isActiveWindow():
                if self.hc or ticker:
                    self.hc = False
                    if self.Exchanges.height():
                        if self._handle(self.exchanges, self.signal.exchange_singal.emit): continue
                        self.exchanges = None
                    if self._handle(self.expands, self.signal.expand_singal.emit): continue
                    self.expands = None
                sleep(0.05)
            else:
                sleep(0.5)

    def text_change(self):
        self.tc = True
        self.set_add_enabled(False)
        self.Translated_text.setText('')
        self.Translated_text.setToolTip('')
        self.Phonetic.setText('')
        self.Phonetic.setToolTip('')
        self.Exchanges.clear()
        self.Expand.clear()
        self.exchanges = self.expands = None

    def command_add(self):
        self.append(self.result)
        self.Word_Entry.setText('')
        self.set_add_enabled(False)
        self.Files.keep()

    def load(self, files:str|list[str]=None):
        states = Publics['ui_states']
        if not files: files = states['files'] if 'files' in states else info.default_voca
        if 'current' in states and (current := states['current']):
            for f in files:
                item = self.Files.load(f)
                if f == current:
                    self.Files.current = item
        self.display_file()

    def store_states(self):
        states = Publics['ui_states']
        states['geometry'] = tuple(self.parent.geometry().getRect()) if not self.parent.isMaximized() else None
        states['text'] = self.Word_Entry.text()
        states['files'] = self.Files.files
        current = self.Files.current
        states['current'] = current.file if current else None
        Publics.dump()

    def restore_states(self):
        states = Publics['ui_states']
        if 'geometry' in states and (geometry := states['geometry']):
            self.parent.setGeometry(*geometry)
        if 'text' in states and (text := states['text']):
            self.Word_Entry.setText(text)

    def check_update(self):
        try: latest = get(info.release_api, timeout=info.timeout, verify=False).json()
        except: latest = None
        self.signal.show_update_singal.emit(latest)

    def show_update(self, latest):
        try:
            ver = latest['tag_name']
            if ver != info.version:
                if QMessageBox.question(self.raw, Setting.getTr('info'), Setting.getTr('update_tip') % ver) \
                    == QMessageBox.StandardButton.Yes:
                    webbrowser.open(latest['html_url'])
            else:
                QMessageBox.information(self.raw, Setting.getTr('info'), Setting.getTr('update_latest'))
        except: QMessageBox.warning(self.raw, Setting.getTr('warning'), Setting.getTr('update_failed'))

    def display_selection(self):
        items = self.Bank.selections
        if items:
            self.Delete.setEnabled(True)
            self.Top.setEnabled(True)
            item = self.Bank.current
            item = item if item else items[-1]
            self.Word_Entry.setText(item.word)
        else:
            self.Delete.setEnabled(False)
            self.Top.setEnabled(False)
    
    def display_exchanges(self):
        items = self.Exchanges.selections
        if items:
            item = self.Exchanges.current
            item = item if item else items[-1]
            self.Word_Entry.setText(item.word)
    
    def display_phrases(self):
        items = self.Expand.selections
        if items:
            item = self.Expand.current
            item = item if item else items[-1]
            self.Word_Entry.setText(item.word)

    def display_file(self):
        item = self.Files.current
        if item and not item.on_display:
            self._display_file(item)

    def _display_file(self, item:FItem):
        for i in self.Files.items:
            i.on_display = False
        item.on_display = True
        self.Bank.results = item.results
