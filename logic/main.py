from PySide6.QtWidgets import QMessageBox, QMainWindow
from PySide6.QtCore import Signal, QObject
from libs.translate.lexicons import load_lexis
from libs.ui.main import Ui_MainWindow
from libs.debris import Ticker
from libs.translate import Result
from libs.configs.settings import Setting
from libs.configs.public import Publics
from win32com.client import Dispatch
from threading import Thread
from requests import get
from time import sleep
import webbrowser, info

class LSignal(QObject):
    set_result_singal = Signal()
    callback_singal = Signal()
    show_lexis_singal = Signal()
    show_update_singal = Signal(dict, bool)
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
    add_enabled = False
    exchanges = None
    expands = None
    parent = None
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
    def check(self): self.set_add_locked(not len(self.Files.items))
    def close(self): info.prog_running = False; self.parent.close()
    def set_expand(self, results):
        if not self.hc and not self.tc: self.Expand.results = results
    def set_exchanges(self, results):
        if not self.hc and not self.tc: self.Exchanges.results = results

    def __init__(self, MainWindow:QMainWindow):
        super().__init__()
        self.setupUi(MainWindow)
        self.parent = MainWindow
        Thread(target=self.check_update, args=(True,)).start()
        Thread(target=self.handle, name='Handle').start()
        self.connect_actions()
    
    def connect_actions(self):
        #Menu Actions
        self.menuRecent.aboutToShow.connect(self.recent_update)
        self.actionNew.triggered.connect(self.Files.new)
        self.actionReload.triggered.connect(self.Files.reload)
        self.actionLoad.triggered.connect(self.Files.open)
        self.actionSave.triggered.connect(self.Files.save)
        self.actionSave_All.triggered.connect(lambda:self.Files.save_all(False))
        self.actionSave_As.triggered.connect(self.Files.save_as)
        self.actionRemove.triggered.connect(self.Files.remove)
        self.actionClear.triggered.connect(self.Files.clear)
        actions = self.menuFile.actions()
        self.Files.menu.addActions(actions[:4] + actions[5:12])
        
        self.actionExit.triggered.connect(self.close)
        self.actionCheck.triggered.connect(lambda:Thread(target=self.check_update).start())
        self.actionAbout.triggered.connect(lambda:webbrowser.open(info.repo_url))
        self.actionAboutQt.triggered.connect(lambda:QMessageBox.aboutQt(self.parent))
        #Button Actions
        self.Add.clicked.connect(self.command_add)
        self.Delete.clicked.connect(self.Bank.remove)
        self.Top.clicked.connect(self.Bank.top)
        #Text
        self.Word_Entry.textChanged.connect(self.text_change)
        self.Translated_text.mouseDoubleClickEvent = self.correct
        self.Phonetic.mouseDoubleClickEvent = lambda *evt:Thread(target=lambda:self._voice.Speak(self.Word_Entry.text()) if self.result else ..., daemon=True).start()
        #List Widgets
        self.Bank.itemSelectionChanged.connect(self.display_selection)
        self.Exchanges.itemSelectionChanged.connect(self.display_exchanges)
        self.Expand.itemSelectionChanged.connect(self.display_phrases)
        #Signal
        self.signal.set_result_singal.connect(self.set_result)
        self.signal.show_update_singal.connect(self.show_update)
        self.signal.callback_singal.connect(lambda:QMessageBox.warning(self.parent, Setting.getTr('warning'), Setting.getTr('translate_function_unavailable')))
        self.signal.exchange_singal.connect(self.set_exchanges)
        self.signal.expand_singal.connect(self.set_expand)

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
        self.set_add_enabled(word not in self.Bank.words and bool(result))

    def correct(self, *evt):
        result = self.result
        if result.match:
            self.Word_Entry.setText(result.word)
        elif result:
            info.clipboard.setText(result.get_translation())

    def set_result(self):
        result = self.result
        if result.match:
            self.Translated_text.setText(result.get_tip())
            self.Translated_text.setToolTip(Setting.getTr('correct_hint'))
            return
        if result:
            self.Phonetic.setToolTip(info.speech_hint % Setting.getTr('speech_hint'))
            self.exchanges = result.exchanges
            self.expands = result.expands
            self.hc = True
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
        self.Bank.append(self.result)
        self.Word_Entry.setText('')
        self.set_add_enabled(False)

    def load(self, files:str|list[str]=None):
        states = Publics['ui_states']
        if not files: files = states['files'] if 'files' in states else [info.default_voca]
        elif isinstance(files, str): files = [files]
        cf = states['current'] if 'current' in states else None
        for i in range(len(files)):
            item = self.Files.load(files[i])
            if cf == i: self.Files.current = item
        self.Files.current = self.Files.current or self.Files.items[0]

    def store_states(self):
        states = Publics['ui_states']
        states['geometry'] = tuple(self.parent.geometry().getRect()) if not self.parent.isMaximized() else None
        states['text'] = self.Word_Entry.text()
        files = self.Files.files
        states['files'] = files
        current = self.Files.current
        states['current'] = files.index(current.file) if current else None
        Publics.dump()

    def restore_states(self):
        states = Publics['ui_states']
        if 'geometry' in states and (geometry := states['geometry']):
            self.parent.setGeometry(*geometry)
        if 'text' in states and (text := states['text']):
            self.Word_Entry.setText(text)

    def check_update(self, silent=False):
        try: latest = get(info.release_api, timeout=info.timeout, verify=False).json()
        except: latest = None
        self.signal.show_update_singal.emit(latest, silent)

    def show_update(self, latest, silent):
        try:
            ver = latest['tag_name']
            if ver > info.version:
                if QMessageBox.question(self.parent, Setting.getTr('info'), Setting.getTr('update_tip') % ver) \
                    == QMessageBox.StandardButton.Yes: webbrowser.open(latest['html_url'])
            elif not silent: QMessageBox.information(self.parent, Setting.getTr('info'), Setting.getTr('update_latest'))
        except:
            if not silent: QMessageBox.warning(self.parent, Setting.getTr('warning'), Setting.getTr('update_failed'))

    def recent_update(self):
        self.menuRecent.clear()
        recent = Publics['recent'] #type: list[str]
        for f in recent:
            action = self.menuRecent.addAction(f.split('/')[-1])
            action.setStatusTip(f)
            action.triggered.connect(lambda *x, f=f:self.load(f))

    def display_selection(self):
        items = self.Bank.selections
        if items:
            self.Delete.setEnabled(True)
            self.Top.setEnabled(True)
            cur_i = self.Bank.currentRow()
            if abs(cur_i-self.Bank.row(items[-1])) == 1: item = items[-1]
            elif abs(cur_i-self.Bank.row(items[0])) == 1: item = items[0]
            else: item = self.Bank.current
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

