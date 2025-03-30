from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QDesktopServices
from libs.ui.main import Ui_MainWindow
from libs.debris import Ticker, Speak
from libs.translate import Result
from libs.configs import *
from libs.io.thread import Thread
from libs.io.requests import get
from time import sleep
import logic, info


class LSignal(QObject):
    setResult = Signal()
    showUpdate = Signal(dict, bool)
    setExchanges = Signal(Result)
    setExpand = Signal(Result)

    def __init__(self):
        super().__init__()


class LMain(Ui_MainWindow):
    result: Result = None
    signal = LSignal()
    exchanges = None
    expands = None
    tc = False
    hc = False

    def __init__(self, parent):
        super().__init__()
        self.setupUi(parent)
        self.parent: logic.LMainWindow = parent
        Thread(self.checkUpdate, True)
        Thread(self.handle)
        self.connectActions()

    def checkAdd(self):
        self.Add.setEnabled(
            bool(len(self.Files.items))
            and bool(self.result)
            and self.result not in self.Bank.words
        )

    def close(self):
        info.prog_running = False
        self.parent.close()

    def speak(self, _):
        if self.result:
            Speak(self.WordEntry.text())

    def textChanged(self):
        self.tc = True

    def setExpand(self, results):
        if not self.hc and not self.tc:
            self.Expand.results = results

    def setExchanges(self, results):
        if not self.hc and not self.tc:
            self.Exchanges.results = results

    def clearRecent(self):
        Publics["recent"] = []

    def connectActions(self):
        # Menu Actions
        self.menuRecent.aboutToShow.connect(self.showRecent)
        self.actionNew.triggered.connect(self.Files.new)
        self.actionReload.triggered.connect(self.Files.reload)
        self.actionLoad.triggered.connect(self.Files.open)
        self.actionSave.triggered.connect(self.Files.save)
        self.actionSaveAll.triggered.connect(self.Files.saveAll)
        self.actionSaveAs.triggered.connect(self.Files.saveAs)
        self.actionRemove.triggered.connect(self.Files.remove)
        self.actionClear.triggered.connect(self.Files.clear)
        self.actionClearRecent.triggered.connect(self.clearRecent)
        actions = self.menuFile.actions()
        self.Files.menu.addActions(actions[:4] + actions[5:12])
        self.actionExit.triggered.connect(self.close)
        self.actionCheck.triggered.connect(lambda: Thread(self.checkUpdate))
        self.actionAbout.triggered.connect(
            lambda: QDesktopServices.openUrl(info.repo_url)
        )
        self.actionAboutQt.triggered.connect(info.app.aboutQt)
        # Button Actions
        self.Add.clicked.connect(self.addCurrent)
        self.Delete.clicked.connect(self.Bank.remove)
        self.Top.clicked.connect(self.Bank.top)
        # Text
        self.WordEntry.textChanged.connect(self.textChanged)
        self.TranslatedText.mouseDoubleClickEvent = self.copyOrCorrect
        self.Phonetic.mouseDoubleClickEvent = self.speak
        # List Widgets
        self.Files.displayChanged.connect(self.checkAdd)
        self.Bank.itemSelectionChanged.connect(self.displaySelection)
        self.Bank.onEdit.connect(self.checkAdd)
        self.Exchanges.itemSelectionChanged.connect(self.displayExchanges)
        self.Expand.itemSelectionChanged.connect(self.displayPhrases)
        # Signal
        self.signal.setResult.connect(self.setResult)
        self.signal.setResult.connect(self.checkAdd)
        self.signal.showUpdate.connect(self.showUpdate)
        self.signal.setExchanges.connect(self.setExchanges)
        self.signal.setExpand.connect(self.setExpand)

    def setShotcuts(self):
        self.Add.setShortcut(Setting.KeyAdd)
        self.Delete.setShortcut(Setting.KeyDel)
        self.Top.setShortcut(Setting.KeyTop)

    def copyOrCorrect(self, _):
        result = self.result
        if result.match:
            self.WordEntry.setText(result.word)
        elif result:
            info.clipboard.setText(result.getTranslation())

    def setResult(self):
        result = self.result
        if result:
            self.TranslatedText.setText(result.getTranslation())
            self.TranslatedText.setToolTip(result.getDefinition())
            self.Phonetic.setText(result.phonetic)
            self.Phonetic.setToolTip(info.speech_hint % Setting.getTr("speech_hint"))
            self.exchanges = result.exchanges
            self.expands = result.expands
        else:
            self.Exchanges.clear()
            self.Expand.clear()
            self.exchanges = self.expands = None
            if result is None:
                self.TranslatedText.setText("")
                self.TranslatedText.setToolTip("")
                self.Phonetic.setText("")
                self.Phonetic.setToolTip("")
            elif result.match:
                self.TranslatedText.setText(result.getTip())
                self.TranslatedText.setToolTip(Setting.getTr("correct_hint"))
        self.hc = True

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
                        if self._handle(self.exchanges, self.signal.setExchanges.emit):
                            continue
                        self.exchanges = None
                    if self._handle(self.expands, self.signal.setExpand.emit):
                        continue
                    self.expands = None
                sleep(0.05)
            else:
                sleep(0.5)

    def addCurrent(self):
        self.Bank.append(self.result)
        self.WordEntry.setText("")

    def loadWithState(self, file):
        states = Publics["ui_states"]
        if file:
            self.Files.loads(file)
        else:
            files = states["files"] if "files" in states else [info.default_voca]
            current = states["current"] if "current" in states else 0
            self.Files.loads(*files, index=current)

    def storeStates(self):
        states = Publics["ui_states"]
        states["geometry"] = (
            tuple(self.parent.geometry().getRect())
            if not self.parent.isMaximized()
            else None
        )
        states["text"] = self.WordEntry.text()
        files = self.Files.files
        states["files"] = files
        current = self.Files.current
        states["current"] = files.index(current.file) if current else None
        Publics.dump()

    def restoreStates(self):
        states = Publics["ui_states"]
        if "geometry" in states and (geometry := states["geometry"]):
            self.parent.setGeometry(*geometry)
        if "text" in states and (text := states["text"]):
            self.WordEntry.setText(text)

    def checkUpdate(self, silent=False):
        latest = get(info.release_api)
        self.signal.showUpdate.emit(latest, silent)

    def showUpdate(self, latest, silent):
        try:
            ver = latest["tag_name"]
            if ver > info.version:
                if self.parent.question(Setting.getTr("update_tip") % ver):
                    QDesktopServices.openUrl(latest["html_url"])
            elif not silent:
                self.parent.information(Setting.getTr("update_latest"))
        except:
            if not silent:
                self.parent.warning(Setting.getTr("update_failed"))

    def showRecent(self):
        for action in self.menuRecent.actions()[2:]:
            self.menuRecent.removeAction(action)
        recent: list[str] = Publics["recent"]
        for f in recent:
            if info.os.path.exists(f):
                action = self.menuRecent.addAction(f.split("/")[-1])
                action.setStatusTip(f)
                action.triggered.connect(lambda _, f=f: self.Files.loads(f))

    def displaySelection(self):
        items = self.Bank.selections
        if items:
            self.Delete.setEnabled(True)
            self.Top.setEnabled(True)
            cur_i = self.Bank.currentRow()
            if abs(cur_i - self.Bank.row(items[-1])) == 1:
                item = items[-1]
            elif abs(cur_i - self.Bank.row(items[0])) == 1:
                item = items[0]
            else:
                item = self.Bank.current
            if item:
                self.WordEntry.setText(item.word)
        else:
            self.Delete.setEnabled(False)
            self.Top.setEnabled(False)

    def displayExchanges(self):
        items = self.Exchanges.selections
        if items:
            item = self.Exchanges.current
            item = item if item else items[-1]
            self.WordEntry.setText(item.word)

    def displayPhrases(self):
        items = self.Expand.selections
        if items:
            item = self.Expand.current
            item = item if item else items[-1]
            self.WordEntry.setText(item.word)
