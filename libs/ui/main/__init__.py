from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.configs import Setting
from .base import Bank, Files, TranslatedText, Phonetic
from . import res


class Ui_MainWindow:
    def __init__(self):
        self.icon = QIcon()
        self.icon.addFile(":/img/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.resize(800, 500)
        MainWindow.setWindowIcon(self.icon)
        self.actionReload = QAction(MainWindow)
        icon1 = QIcon(QIcon.fromTheme("view-refresh"))
        self.actionReload.setIcon(icon1)
        self.actionReload.setShortcut("Ctrl+R")
        self.actionSave = QAction(MainWindow)
        icon2 = QIcon(QIcon.fromTheme("document-save"))
        self.actionSave.setIcon(icon2)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        self.actionLoad = QAction(MainWindow)
        icon3 = QIcon(QIcon.fromTheme("document-open"))
        self.actionLoad.setIcon(icon3)
        self.actionLoad.setShortcut("Ctrl+L")
        self.actionSaveAs = QAction(MainWindow)
        icon4 = QIcon(QIcon.fromTheme("document-save-as"))
        self.actionSaveAs.setIcon(icon4)
        self.actionClear = QAction(MainWindow)
        icon5 = QIcon(QIcon.fromTheme("edit-clear"))
        self.actionClear.setIcon(icon5)
        self.actionClear.setShortcut("Ctrl+Shift+W")
        self.actionExit = QAction(MainWindow)
        icon6 = QIcon(QIcon.fromTheme("system-shutdown"))
        self.actionExit.setIcon(icon6)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionSetting = QAction(MainWindow)
        icon7 = QIcon(QIcon.fromTheme("document-properties"))
        self.actionSetting.setIcon(icon7)
        self.actionAbout = QAction(MainWindow)
        icon8 = QIcon(QIcon.fromTheme("emblem-important"))
        self.actionAbout.setIcon(icon8)
        self.actionAboutQt = QAction(MainWindow)
        icon9 = QIcon(QIcon.fromTheme("system-help"))
        self.actionAboutQt.setIcon(icon9)
        self.actionRemove = QAction(MainWindow)
        icon10 = QIcon(QIcon.fromTheme("list-remove"))
        self.actionRemove.setIcon(icon10)
        self.actionRemove.setShortcut("Ctrl+W")
        self.actionNew = QAction(MainWindow)
        icon11 = QIcon(QIcon.fromTheme("document-new"))
        self.actionNew.setIcon(icon11)
        self.actionNew.setShortcut("Ctrl+N")
        self.actionSaveAll = QAction(MainWindow)
        self.actionSaveAll.setIcon(icon2)
        self.actionSaveAll.setShortcut("Ctrl+Alt+S")
        self.actionCheck = QAction(MainWindow)
        icon12 = QIcon(QIcon.fromTheme("emblem-favorite"))
        self.actionCheck.setIcon(icon12)
        self.actionClearRecent = QAction(MainWindow)
        icon13 = QIcon(QIcon.fromTheme("document-open-recent"))
        self.actionClearRecent.setIcon(icon13)
        self.centralwidget = QWidget(MainWindow)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.WordEntry = QLineEdit(self.centralwidget)
        self.WordEntry.setMinimumSize(QSize(100, 31))
        self.WordEntry.setMaximumSize(QSize(16777215, 31))
        font = QFont()
        font.setFamilies(["Microsoft YaHei UI"])
        font.setPointSize(11)
        self.WordEntry.setFont(font)
        self.WordEntry.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.WordEntry.setStyleSheet(
            "color: rgb(0, 255, 0);background-color: rgba(52, 255, 52, 50);"
        )

        self.gridLayout.addWidget(self.WordEntry, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.Add = QPushButton(self.centralwidget)
        self.Add.setEnabled(False)
        self.Add.setMinimumSize(QSize(0, 32))
        self.Add.setMaximumSize(QSize(16777215, 32))
        self.Add.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Add.setStyleSheet(
            "font: 10pt;color: rgb(255, 170, 0);background-color: rgba(255, 170, 20, 50);"
        )
        icon14 = QIcon(QIcon.fromTheme("list-add"))
        self.Add.setIcon(icon14)

        self.verticalLayout_2.addWidget(self.Add)

        self.Top = QPushButton(self.centralwidget)
        self.Top.setEnabled(False)
        self.Top.setMinimumSize(QSize(0, 32))
        self.Top.setMaximumSize(QSize(16777215, 32))
        self.Top.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Top.setStyleSheet(
            "font: 10pt;color: rgb(0, 170, 255);background-color: rgba(0, 170, 255, 50);"
        )
        icon15 = QIcon(QIcon.fromTheme("appointment-new"))
        self.Top.setIcon(icon15)

        self.verticalLayout_2.addWidget(self.Top)

        self.Delete = QPushButton(self.centralwidget)
        self.Delete.setEnabled(False)
        self.Delete.setMinimumSize(QSize(0, 31))
        self.Delete.setMaximumSize(QSize(16777215, 31))
        self.Delete.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Delete.setStyleSheet(
            "font: 10pt;color: rgb(255, 0, 0);background-color: rgba(255, 0, 0, 50);"
        )
        icon16 = QIcon(QIcon.fromTheme("edit-delete"))
        self.Delete.setIcon(icon16)

        self.verticalLayout_2.addWidget(self.Delete)
        self.Bank = Bank(self.centralwidget)
        self.Bank.setMinimumSize(QSize(128, 0))
        self.Bank.setMaximumSize(QSize(128, 16777215))
        self.Bank.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Bank.setStyleSheet(
            "QToolTip{background-color: rgba(30,30,30,100);color: rgb(85, 255, 255);}QListWidget{font: 10pt;color: rgb(85, 255, 255);}"
        )
        self.Bank.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Bank.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Bank.setAutoScroll(False)
        self.Bank.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Bank.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.Bank.setSortingEnabled(True)

        self.gridLayout.addWidget(self.Bank, 0, 2, 2, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.Exchanges = Bank(self.splitter)
        self.Exchanges.setMinimumSize(QSize(128, 0))
        self.Exchanges.setMaximumSize(QSize(128, 16777215))
        self.Exchanges.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Exchanges.setStyleSheet(
            "QToolTip{background-color: rgba(30,30,30,100);color: rgb(170, 255, 127);}QListWidget{font: 10pt;color: rgb(170, 255, 127);}"
        )
        self.Exchanges.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Exchanges.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.Exchanges.setAutoScroll(False)
        self.Exchanges.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Exchanges.setSortingEnabled(True)
        self.splitter.addWidget(self.Exchanges)
        self.Files = Files(self.splitter, self.Bank)
        self.Files.setMinimumSize(QSize(128, 51))
        self.Files.setMaximumSize(QSize(128, 16777215))
        self.Files.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Files.setStyleSheet(
            "QToolTip{background-color: rgba(30,30,30,100);color: rgb(255, 85, 255);}QListWidget{font: 10pt;color: rgb(255, 85, 255);}"
        )
        self.Files.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Files.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Files.setAutoScroll(False)
        self.Files.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Files.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.splitter.addWidget(self.Files)

        self.verticalLayout_2.addWidget(self.splitter)

        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 2, 1)

        self.Expand = Bank(self.centralwidget)
        self.Expand.setMinimumSize(QSize(150, 0))
        self.Expand.setMaximumSize(QSize(150, 16777215))
        self.Expand.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.Expand.setStyleSheet(
            "QToolTip{background-color: rgba(30,30,30,100);color: rgb(200, 200, 25);}QListWidget{font: 10pt;color: rgb(200, 200, 25);}"
        )
        self.Expand.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Expand.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Expand.setAutoScroll(False)
        self.Expand.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Expand.setSortingEnabled(True)

        self.gridLayout.addWidget(self.Expand, 0, 3, 2, 1)

        self.verticalLayout = QVBoxLayout()
        self.TranslatedText = TranslatedText(self.centralwidget)
        self.TranslatedText.setMinimumSize(QSize(0, 117))
        self.TranslatedText.setStyleSheet(
            "QLabel{font: 75 12pt;color: rgb(0, 170, 255);}QToolTip{background-color: rgba(30,30,30,100);color: rgb(0, 170, 255);}"
        )
        self.TranslatedText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TranslatedText.setWordWrap(True)

        self.verticalLayout.addWidget(self.TranslatedText)

        self.Phonetic = Phonetic(self.centralwidget)
        self.Phonetic.setMinimumSize(QSize(172, 42))
        self.Phonetic.setMaximumSize(QSize(16777215, 42))
        self.Phonetic.setStyleSheet(
            "QLabel{font: 700 12pt;color: rgb(255, 170, 0);}QToolTip{background-color: rgba(30,30,30,100);color: rgb(255, 170, 0);}"
        )
        self.Phonetic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Phonetic.setWordWrap(True)

        self.verticalLayout.addWidget(self.Phonetic)

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 800, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setToolTipsVisible(False)
        self.menuRecent = QMenu(self.menuFile)
        self.menuTools = QMenu(self.menuBar)
        self.menuTools.setAutoFillBackground(False)
        self.menuTools.setSeparatorsCollapsible(False)
        self.menuTools.setToolTipsVisible(False)
        self.menuSettings = QMenu(self.menuBar)
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionReload)
        self.menuFile.addAction(self.menuRecent.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAll)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRemove)
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuRecent.addAction(self.actionClearRecent)
        self.menuRecent.addSeparator()
        self.menuSettings.addAction(self.actionSetting)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionCheck)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionAboutQt)

    def retranslateUi(self):
        self.actionReload.setText(Setting.translateUI("Reload"))
        self.actionReload.setStatusTip(Setting.translateUI("Reload File"))
        self.actionSave.setText(Setting.translateUI("Save"))
        self.actionSave.setStatusTip(Setting.translateUI("Save File"))
        self.actionLoad.setText(Setting.translateUI("Load"))
        self.actionLoad.setStatusTip(Setting.translateUI("Load Files"))
        self.actionSaveAs.setText(Setting.translateUI("Save As"))
        self.actionSaveAs.setStatusTip(Setting.translateUI("Save File As ..."))
        self.actionClear.setText(Setting.translateUI("Clear"))
        self.actionClear.setStatusTip(Setting.translateUI("Clear Files"))
        self.actionExit.setText(Setting.translateUI("Exit"))
        self.actionExit.setStatusTip(Setting.translateUI("Exit"))
        self.actionSetting.setText(Setting.translateUI("Settings"))
        self.actionSetting.setStatusTip(Setting.translateUI("Settings"))
        self.actionAbout.setText(Setting.translateUI("About"))
        self.actionAbout.setStatusTip(Setting.translateUI("About This Programm"))
        self.actionAboutQt.setText(Setting.translateUI("About Qt"))
        self.actionAboutQt.setStatusTip(Setting.translateUI("About Qt Engine"))
        self.actionRemove.setText(Setting.translateUI("Remove"))
        self.actionRemove.setStatusTip(Setting.translateUI("Remove Current File"))
        self.actionNew.setText(Setting.translateUI("New"))
        self.actionNew.setStatusTip(Setting.translateUI("Create a New File"))
        self.actionSaveAll.setText(Setting.translateUI("Save All"))
        self.actionSaveAll.setStatusTip(Setting.translateUI("Save All Files"))
        self.actionCheck.setText(Setting.translateUI("Check Update"))
        self.actionCheck.setStatusTip(Setting.translateUI("Check the Latest Version"))
        self.actionClearRecent.setText(Setting.translateUI("Clear"))
        self.actionClearRecent.setStatusTip(Setting.translateUI("Clear Recent Records"))
        self.WordEntry.setStatusTip(Setting.translateUI("Word Entry"))
        self.WordEntry.setPlaceholderText(Setting.translateUI("Enter a word"))
        self.Add.setStatusTip(Setting.translateUI("Add into Vocabulary"))
        self.Add.setText(Setting.translateUI("Add"))
        self.Bank.setStatusTip(Setting.translateUI("Vocabulary Bank"))
        self.TranslatedText.setStatusTip(Setting.translateUI("Translations"))
        self.Phonetic.setStatusTip(Setting.translateUI("Phonetic"))
        self.Top.setStatusTip(Setting.translateUI("Top the Words"))
        self.Top.setText(Setting.translateUI("Top"))
        self.Delete.setStatusTip(Setting.translateUI("Delete the Words"))
        self.Delete.setText(Setting.translateUI("Delete"))
        self.Exchanges.setStatusTip(Setting.translateUI("Exchanges"))
        self.Files.setStatusTip(Setting.translateUI("Files"))
        self.Expand.setStatusTip(Setting.translateUI("Expand"))
        self.menuFile.setTitle(Setting.translateUI("File"))
        self.menuRecent.setTitle(Setting.translateUI("Recent"))
        self.menuTools.setTitle(Setting.translateUI("Tools"))
        self.menuSettings.setTitle(Setting.translateUI("Settings"))
