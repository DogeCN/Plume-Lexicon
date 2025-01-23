from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.configs.settings import Setting
from . import res


class Ui_Settings(object):
    def setupUi(self, Settings: QDialog):
        if not Settings.objectName():
            Settings.setObjectName("Settings")
        Settings.resize(520, 430)
        icon = QIcon(QIcon.fromTheme("document-properties"))
        Settings.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName("gridLayout")
        self.lInterface = QLabel(Settings)
        self.lInterface.setObjectName("lInterface")
        self.lInterface.setMinimumSize(QSize(218, 0))
        self.lInterface.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lInterface, 0, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

        self.gridLayout.addWidget(self.buttonBox, 0, 2, 2, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lLang = QLabel(Settings)
        self.lLang.setObjectName("lLang")
        self.lLang.setMaximumSize(QSize(57, 16777215))

        self.horizontalLayout_5.addWidget(self.lLang)

        self.Lang = QComboBox(Settings)
        icon1 = QIcon()
        icon1.addFile(":/icon/Chinese.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Lang.addItem(icon1, "\u7b80\u4f53\u4e2d\u6587")
        icon2 = QIcon()
        icon2.addFile(":/icon/English.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Lang.addItem(icon2, "English")
        self.Lang.setObjectName("Lang")

        self.horizontalLayout_5.addWidget(self.Lang)

        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lTheme = QLabel(Settings)
        self.lTheme.setObjectName("lTheme")
        self.lTheme.setMaximumSize(QSize(57, 16777215))

        self.horizontalLayout_4.addWidget(self.lTheme)

        self.themeAcrylic = QRadioButton(Settings)
        self.themeAcrylic.setObjectName("themeAcrylic")

        self.horizontalLayout_4.addWidget(self.themeAcrylic)

        self.themeDark = QRadioButton(Settings)
        self.themeDark.setObjectName("themeDark")

        self.horizontalLayout_4.addWidget(self.themeDark)

        self.themeFusion = QRadioButton(Settings)
        self.themeFusion.setObjectName("themeFusion")
        self.themeFusion.setText("Fusion")

        self.horizontalLayout_4.addWidget(self.themeFusion)

        self.themeDefault = QRadioButton(Settings)
        self.themeDefault.setObjectName("themeDefault")

        self.horizontalLayout_4.addWidget(self.themeDefault)

        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)

        self.lFile = QLabel(Settings)
        self.lFile.setObjectName("lFile")
        self.lFile.setMinimumSize(QSize(218, 0))
        self.lFile.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lFile, 3, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lAuto = QLabel(Settings)
        self.lAuto.setObjectName("lAuto")
        self.lAuto.setMaximumSize(QSize(58, 16777215))

        self.horizontalLayout_2.addWidget(self.lAuto)

        self.Auto_Save = QCheckBox(Settings)
        self.Auto_Save.setObjectName("Auto_Save")
        self.Auto_Save.setMaximumSize(QSize(40, 20))
        icon3 = QIcon(QIcon.fromTheme("document-save"))
        self.Auto_Save.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.Auto_Save)

        self.Interval = QSpinBox(Settings)
        self.Interval.setObjectName("Interval")
        self.Interval.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.Interval.setMinimum(10)
        self.Interval.setMaximum(99)

        self.horizontalLayout_2.addWidget(self.Interval)

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lCache = QLabel(Settings)
        self.lCache.setObjectName("lCache")
        self.lCache.setMaximumSize(QSize(58, 16777215))

        self.horizontalLayout_3.addWidget(self.lCache)

        self.CClear = QPushButton(Settings)
        self.CClear.setObjectName("CClear")
        icon4 = QIcon(QIcon.fromTheme("user-trash"))
        self.CClear.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.CClear)

        self.viewCache = QToolButton(Settings)
        self.viewCache.setObjectName("viewCache")
        icon5 = QIcon(QIcon.fromTheme("folder-open"))
        self.viewCache.setIcon(icon5)
        self.viewCache.setIconSize(QSize(30, 16))

        self.horizontalLayout_3.addWidget(self.viewCache)

        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 2)

        self.lHot = QLabel(Settings)
        self.lHot.setObjectName("lHot")
        self.lHot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lHot, 6, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lAdd = QLabel(Settings)
        self.lAdd.setObjectName("lAdd")

        self.verticalLayout_2.addWidget(self.lAdd)

        self.lDel = QLabel(Settings)
        self.lDel.setObjectName("lDel")

        self.verticalLayout_2.addWidget(self.lDel)

        self.lTop = QLabel(Settings)
        self.lTop.setObjectName("lTop")

        self.verticalLayout_2.addWidget(self.lTop)

        self.gridLayout.addLayout(self.verticalLayout_2, 7, 0, 3, 1)

        self.Key_Add = QKeySequenceEdit(Settings)
        self.Key_Add.setObjectName("Key_Add")

        self.gridLayout.addWidget(self.Key_Add, 7, 1, 1, 1)

        self.Key_Delete = QKeySequenceEdit(Settings)
        self.Key_Delete.setObjectName("Key_Delete")

        self.gridLayout.addWidget(self.Key_Delete, 8, 1, 1, 1)

        self.Key_Top = QKeySequenceEdit(Settings)
        self.Key_Top.setObjectName("Key_Top")

        self.gridLayout.addWidget(self.Key_Top, 9, 1, 1, 1)

        self.lTranslate = QLabel(Settings)
        self.lTranslate.setObjectName("lTranslate")
        self.lTranslate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lTranslate, 10, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Online = QCheckBox(Settings)
        self.Online.setObjectName("Online")
        icon6 = QIcon(QIcon.fromTheme("applications-internet"))
        self.Online.setIcon(icon6)

        self.horizontalLayout.addWidget(self.Online)

        self.LReload = QPushButton(Settings)
        self.LReload.setObjectName("LReload")
        icon7 = QIcon(QIcon.fromTheme("view-refresh"))
        self.LReload.setIcon(icon7)

        self.horizontalLayout.addWidget(self.LReload)

        self.viewLexicons = QToolButton(Settings)
        self.viewLexicons.setObjectName("viewLexicons")
        self.viewLexicons.setIcon(icon5)
        self.viewLexicons.setIconSize(QSize(30, 16))

        self.horizontalLayout.addWidget(self.viewLexicons)

        self.gridLayout.addLayout(self.horizontalLayout, 11, 0, 1, 2)

        self.LexiconBox = QGroupBox(Settings)
        self.LexiconBox.setObjectName("LexiconBox")
        self.verticalLayout_3 = QVBoxLayout(self.LexiconBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.Lexicons = QScrollArea(self.LexiconBox)
        self.Lexicons.setObjectName("Lexicons")
        self.Lexicons.setFrameShape(QFrame.Shape.NoFrame)
        self.Lexicons.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Lexicons.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.Lexicons.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 401, 64))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Lexicons.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.Lexicons)

        self.gridLayout.addWidget(self.LexiconBox, 12, 0, 1, 2)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)

    def retranslateUi(self, Settings: QDialog):
        Settings.setWindowTitle(Setting.translateUI("Settings"))
        self.lInterface.setText(Setting.translateUI("Interface"))
        self.lLang.setText(Setting.translateUI("Language"))
        self.lTheme.setText(Setting.translateUI("Theme"))
        self.themeAcrylic.setText(Setting.translateUI("Acrylic"))
        self.themeDark.setText(Setting.translateUI("Dark"))
        self.themeDefault.setText(Setting.translateUI("Default"))
        self.lFile.setText(Setting.translateUI("Files"))
        self.lAuto.setText(Setting.translateUI("Auto Save"))
        self.Interval.setSuffix(Setting.translateUI(" Secs"))
        self.lAdd.setText(Setting.translateUI("Add"))
        self.lDel.setText(Setting.translateUI("Delete"))
        self.lTop.setText(Setting.translateUI("Top"))
        self.Online.setText(Setting.translateUI("Online"))
        self.LReload.setText(Setting.translateUI("Reload Lexicons"))
        self.LexiconBox.setTitle(Setting.translateUI("Lexicons"))
        self.lHot.setText(Setting.translateUI("Hotkeys"))
        self.lTranslate.setText(Setting.translateUI("Translate"))
        self.CClear.setText(Setting.translateUI("Clear"))
        self.lCache.setText(Setting.translateUI("Cache"))
