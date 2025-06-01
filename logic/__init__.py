from __future__ import annotations
from PySide6.QtWidgets import QMessageBox, QDialog, QMenu, QMainWindow, QSystemTrayIcon
from PySide6.QtCore import QEvent
from libs.debris import Ticker, Explore, Register
from libs.translate.lexicons import LexiBox, loadLexis, csignal
from libs.translate import trans
from libs.configs import Setting
from libs.ui import Theme
from libs.ui.settings import UISettings
from libs.io.thread import Scheduler, Thread, Worker
from libs.io.stdout import print
from .main import LMain
from time import sleep
import info


class LMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LMain(self)
        self.tray = QSystemTrayIcon(self.ui.icon, self)
        self.tmenu = QMenu(self)
        self.tmenu.addAction(self.ui.actionExit)
        self.tray.setContextMenu(self.tmenu)
        self.setting = QDialog(self)
        self.settingUi = UISettings()
        self.settingUi.setupUi(self.setting)
        self.connectActions()
        self.lboxes: list[LexiBox] = []
        loadLexis()
        Worker(lambda: Register(info.ext_voca, info.cmd) if info.exe else ...)
        Worker(self.ui.loadWithState, info.argv1)
        Theme.AddAcrylic(self)
        Theme.Set(Setting.Theme)
        self.ui.restoreStates()
        self.retrans()
        self.ui.setShotcuts()
        self.ui.Bank.initMenu()
        self.show()
        Thread(self.autoTranslate)
        self.saver = Scheduler(
            lambda: self.ui.Files.saveAll(True) if Setting.AutoSave else ...,
            Setting.AutoSaveInterval * 1000,
        )
        Scheduler(self.check)

    def connectActions(self):
        self.themes = [
            self.settingUi.themeAcrylic,
            self.settingUi.themeDark,
            self.settingUi.themeFusion,
            self.settingUi.themeDefault,
        ]
        self.tray.activated.connect(self.trayActivated)
        self.ui.actionSetting.triggered.connect(self.settingShow)
        self.settingUi.Lang.currentIndexChanged.connect(lambda i: self.retrans(i))
        self.settingUi.buttonBox.accepted.connect(self.accept)
        self.settingUi.buttonBox.rejected.connect(self.setting.hide)
        self.settingUi.Online.toggled.connect(self.setOnline)
        self.settingUi.LReload.clicked.connect(loadLexis)
        self.settingUi.viewLexicons.clicked.connect(lambda: Explore(info.lexis_dir))
        self.settingUi.AutoSave.stateChanged.connect(
            lambda: self.settingUi.Interval.setEnabled(
                self.settingUi.AutoSave.isChecked()
            )
        )
        self.themes[Setting.Theme].setChecked(True)
        for i in range(len(self.themes)):
            self.themes[i].toggled.connect(
                lambda _, i=i: Theme.Set(i)
                or setattr(Setting, "Theme", i)
                or Setting.dump()
            )
        csignal.sre.connect(self.settingUi.LReload.setEnabled)
        csignal.update.connect(self.showLexicons)
        csignal.warn.connect(self.warning)
        info.app.commitDataRequest.connect(self.saveData)

    def check(self):
        action = open(info.running).readline().strip("\n")
        if action:
            if action != info.running_sign and info.os.path.exists(action):
                self.ui.Files.loads(action)
            self.activateWindow()
            self.showNormal()
        open(info.running, "w").write("")

    def trayActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.activateWindow()
            self.showNormal()
            self.tray.hide()

    def accept(self):
        Setting.AutoSave = self.settingUi.AutoSave.isChecked()
        Setting.AutoSaveInterval = self.settingUi.Interval.value()
        self.saver.setInterval(Setting.AutoSaveInterval * 1000)
        Setting.KeyAdd = self.settingUi.KeyAdd.keySequence().toString()
        Setting.KeyDel = self.settingUi.KeyDelete.keySequence().toString()
        Setting.KeyTop = self.settingUi.KeyTop.keySequence().toString()
        self.ui.setShotcuts()
        Setting.dump()

    def settingShow(self):
        self.settingUi.Lang.setCurrentIndex(Setting.Language)
        self.settingUi.AutoSave.setChecked(Setting.AutoSave)
        self.settingUi.Interval.setEnabled(Setting.AutoSave)
        self.settingUi.Interval.setValue(Setting.AutoSaveInterval)
        self.settingUi.KeyAdd.setKeySequence(Setting.KeyAdd)
        self.settingUi.KeyDelete.setKeySequence(Setting.KeyDel)
        self.settingUi.KeyTop.setKeySequence(Setting.KeyTop)
        self.settingUi.Online.setChecked(Setting.Online)
        self.setting.show()
        Theme.AddAcrylic(self.setting)

    def showTools(self):
        from libs.tool import Tools

        for action in self.ui.menuTools.actions()[2:]:
            self.ui.menuTools.removeAction(action)
        for tl in Tools:
            tl.mw = self
            action = tl.action()
            if tl.type:
                self.ui.menuTools.addMenu(action)
            else:
                self.ui.menuTools.addAction(action)

    def showLexicons(self):
        for a in self.lboxes:
            self.settingUi.verticalLayout.removeWidget(a)
            a.deleteLater()
        self.lboxes.clear()
        from libs.translate.lexicons import lexicons

        for l in lexicons:
            lb = LexiBox(self.setting, l)
            self.lboxes.append(lb)
            self.settingUi.verticalLayout.addWidget(lb)

    def retrans(self, lang=None):
        if lang is not None:
            Setting.Language = lang
        self.settingUi.retranslateUi(self.setting)
        self.ui.retranslateUi()
        self.ui.Bank.update()
        self.ui.Exchanges.update()
        self.ui.Expand.update()
        self.ui.Files.update()
        for lb in self.lboxes:
            lb.update()
        title = f"{Setting.getTr('title')} {info.version}"
        self.setWindowTitle(title)
        self.tray.setToolTip(title)
        self.showTools()

    def autoTranslate(self):
        ticker = Ticker()
        while info.prog_running:
            if self.isActiveWindow() or self.setting.isActiveWindow():
                ticking = bool(ticker)
                if self.ui.tc or ticking:
                    self.ui.tc = False
                    word = self.ui.WordEntry.text().strip()
                    if word != "":
                        if (not ticking) and (word not in self.ui.Bank.words):
                            self.ui.Bank.roll(word)
                        self.ui.result = trans(word, self.ui.Bank.results)
                        if self.ui.tc:
                            continue
                    else:
                        self.ui.result = None
                    self.ui.signal.setResult.emit()
                sleep(0.05)
            else:
                sleep(0.5)

    def setOnline(self, o):
        if o:
            csignal.lock()
        else:
            csignal.unlock()
        self.settingUi.LexiconBox.setEnabled(not o)
        Setting.Online = o
        Setting.dump()

    def question(self, msg):
        return (
            QMessageBox.question(self, Setting.getTr("info"), msg)
            == QMessageBox.StandardButton.Yes
        )

    def information(self, msg):
        QMessageBox.information(self, Setting.getTr("info"), msg)

    def warning(self, msg):
        QMessageBox.warning(self, Setting.getTr("warning"), msg)

    def closeEvent(self, evt: QEvent):
        if info.prog_running:
            self.hide()
            self.tray.show()
            evt.ignore()
        else:
            self.saveData()
            print("Process Finished", "Green")
            info.app.exit()

    def saveData(self, *_):
        if Setting.AutoSave:
            self.ui.Files.saveAll()
        self.ui.storeStates()
        print("Data Saved", "Blue")
