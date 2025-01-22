from __future__ import annotations
from PySide6.QtWidgets import QMessageBox, QDialog, QMenu, QMainWindow, QSystemTrayIcon
from PySide6.QtCore import QEvent
from libs.debris import Ticker, Clean_Dir, Convert_Size, Explore
from libs.translate.lexicons import LexiBox, csignal
from libs.translate import trans
from libs.configs.settings import Setting
from libs.tool import load
from libs.ui import Theme
from libs.ui.settings import Ui_Settings
from libs.io.thread import Scheduler, Thread
from .main import LMain
from time import sleep
import info

class LMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #Window Build
        self.ui = LMain(self)
        self.tray = QSystemTrayIcon(self.ui.icon, self)
        self.tmenu = QMenu(self)
        self.tmenu.addAction(self.ui.actionExit)
        self.tray.setContextMenu(self.tmenu)
        #Setting
        self.setting = QDialog(self)
        self.setting_ui = Ui_Settings()
        self.setting_ui.setupUi(self.setting)
        #Threading
        Thread(self.ui.load_lexis)
        Thread(self.ui.load, info.argv1)
        Thread(self.auto_translate)
        self.saver = Scheduler(lambda:self.ui.Files.save_all() if Setting.Auto_save else ...,
                            Setting.Auto_save_interval*1000)
        Scheduler(self.check)
        #UI
        Theme.AddAcrylic(self)
        Theme.Set(Setting.Theme)
        self.lboxes = [] #type: list[LexiBox]
        self.connect_actions()
        self.retrans()
        self.ui.Bank.init_menu()
        self.ui.setShotcuts()
        self.ui.restore_states()
        self.show()

    def connect_actions(self):
        self.themes = [self.setting_ui.themeAcrylic, self.setting_ui.themeDark,
                    self.setting_ui.themeFusion, self.setting_ui.themeDefault]
        self.tray.activated.connect(self.tray_activated)
        self.ui.actionSetting.triggered.connect(self.setting_show)
        self.ui.actionTool_Reload.triggered.connect(lambda:load() or self.show_tools())
        self.ui.signal.show_lexis_singal.connect(self.show_lexicons)
        self.setting_ui.Lang.currentIndexChanged.connect(lambda:self.retrans(self.setting_ui.Lang.currentIndex()))
        self.setting_ui.buttonBox.accepted.connect(self.accept)
        self.setting_ui.buttonBox.rejected.connect(self.setting.hide)
        self.setting_ui.Online.toggled.connect(self.set_online)
        self.setting_ui.LReload.clicked.connect(self.reload_lexis)
        self.setting_ui.viewLexicons.clicked.connect(lambda:Explore(info.lexis_dir))
        self.setting_ui.viewCache.clicked.connect(lambda:Explore(info.cache_dir))
        self.setting_ui.CClear.clicked.connect(lambda:QMessageBox.information(self, Setting.getTr('info'), Setting.getTr('cache_cleared')%Convert_Size(Clean_Dir(info.cache_dir))))
        self.setting_ui.Auto_Save.stateChanged.connect(lambda:self.setting_ui.Interval.setEnabled(self.setting_ui.Auto_Save.isChecked()))
        self.themes[Setting.Theme].setChecked(True)
        for i in range(len(self.themes)): self.themes[i].toggled.connect(lambda *x, i=i:Theme.Set(i) or setattr(Setting, 'Theme', i) or Setting.dump())
        csignal.sre.connect(self.setting_ui.LReload.setEnabled)

    def check(self):
        action = open(info.running).readline().strip('\n')
        if action:
            if action != info.running_sign and info.os.path.exists(action):
                self.ui.load(action)
            self.activateWindow()
            self.showNormal()
        open(info.running, 'w').write('')
        self.ui.set_add_locked(not len(self.ui.Files.items))

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.activateWindow()
            self.showNormal()
            self.tray.hide()

    def accept(self):
        Setting.Auto_save = self.setting_ui.Auto_Save.isChecked()
        Setting.Auto_save_interval = self.setting_ui.Interval.value()
        self.saver.setInterval(Setting.Auto_save_interval*1000)
        Setting.Key_Add = self.setting_ui.Key_Add.keySequence().toString()
        Setting.Key_Del = self.setting_ui.Key_Delete.keySequence().toString()
        Setting.Key_Top = self.setting_ui.Key_Top.keySequence().toString()
        self.ui.setShotcuts()
        Setting.dump()

    def setting_show(self):
        self.setting_ui.Lang.setCurrentIndex(Setting.Language)
        self.setting_ui.Auto_Save.setChecked(Setting.Auto_save)
        self.setting_ui.Interval.setEnabled(Setting.Auto_save)
        self.setting_ui.Interval.setValue(Setting.Auto_save_interval)
        self.setting_ui.Key_Add.setKeySequence(Setting.Key_Add)
        self.setting_ui.Key_Delete.setKeySequence(Setting.Key_Del)
        self.setting_ui.Key_Top.setKeySequence(Setting.Key_Top)
        self.setting_ui.Online.setChecked(Setting.Online)
        self.setting.show()
        Theme.AddAcrylic(self.setting)

    def show_tools(self):
        for action in self.ui.menuTools.actions()[2:]:
            self.ui.menuTools.removeAction(action)
        from libs.tool import Tools
        for tl in Tools:
            tl.mw = self
            action = tl.action()
            if tl.type: self.ui.menuTools.addMenu(action)
            else: self.ui.menuTools.addAction(action)

    def reload_lexis(self):
        for a in self.lboxes:
            self.setting_ui.verticalLayout.removeWidget(a)
            a.deleteLater()
        self.lboxes.clear()
        Thread(self.ui.load_lexis)

    def show_lexicons(self):
        from libs.translate.lexicons import lexicons
        for l in lexicons:
            lb = LexiBox(l, self)
            self.lboxes.append(lb)
            self.setting_ui.verticalLayout.addWidget(lb)

    def retrans(self, lang=None):
        if lang is not None:
            Setting.Language = lang
        self.setting_ui.retranslateUi(self.setting)
        self.ui.retranslateUi()
        for lb in self.lboxes:
            lb.update()
        title = f'{Setting.getTr('title')} {info.version}'
        self.setWindowTitle(title)
        self.tray.setToolTip(title)
        self.show_tools()

    def auto_translate(self):
        ticker = Ticker()
        while info.prog_running:
            #Auto Translate
            if self.isActiveWindow() or self.setting.isActiveWindow():
                ticking = bool(ticker)
                if self.ui.tc or ticking:
                    self.ui.tc = False
                    word = self.ui.Word_Entry.text().strip()
                    if word != '':
                        if (not ticking) and (word not in self.ui.Bank.words):
                            self.ui.Bank.roll(word)
                        self.ui._result = trans(word, self.ui.Bank.results)
                        if self.ui.tc:
                            continue
                        self.ui.signal.set_result_singal.emit()
                sleep(0.05)
            else:
                sleep(0.5)

    def set_online(self, o):
        if o: csignal.lock()
        else: csignal.unlock()
        self.setting_ui.LexiconBox.setEnabled(not o)
        Setting.Online = o
        Setting.dump()

    def closeEvent(self, evt:QEvent):
        if info.prog_running:
            self.hide()
            self.tray.show()
            evt.ignore()
        else:
            if Setting.Auto_save:
                self.ui.Files.save_all(False)
            self.ui.store_states()
            info.app.exit()
