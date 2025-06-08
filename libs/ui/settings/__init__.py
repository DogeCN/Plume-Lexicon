from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.configs import Setting
from . import res


class UISettings(object):
    def setupUi(self, Settings: QDialog):
        Settings.resize(520, 430)
        icon = QIcon(QIcon.fromTheme("document-properties"))
        Settings.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Settings)
        self.lInterface = QLabel(Settings)
        self.lInterface.setMinimumSize(QSize(218, 0))
        self.lInterface.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lInterface, 0, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

        self.gridLayout.addWidget(self.buttonBox, 0, 2, 2, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.lLang = QLabel(Settings)
        self.lLang.setMaximumSize(QSize(57, 16777215))

        self.horizontalLayout_5.addWidget(self.lLang)

        self.Lang = QComboBox(Settings)
        icon1 = QIcon()
        icon1.addFile(":/icon/Chinese.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Lang.addItem(icon1, "\u7b80\u4f53\u4e2d\u6587")
        icon2 = QIcon()
        icon2.addFile(":/icon/English.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Lang.addItem(icon2, "English")

        self.horizontalLayout_5.addWidget(self.Lang)

        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.lTheme = QLabel(Settings)
        self.lTheme.setMaximumSize(QSize(57, 16777215))

        self.horizontalLayout_4.addWidget(self.lTheme)

        self.themeAcrylic = QRadioButton(Settings)

        self.horizontalLayout_4.addWidget(self.themeAcrylic)

        self.themeDark = QRadioButton(Settings)

        self.horizontalLayout_4.addWidget(self.themeDark)

        self.themeFusion = QRadioButton(Settings)
        self.themeFusion.setText("Fusion")

        self.horizontalLayout_4.addWidget(self.themeFusion)

        self.themeDefault = QRadioButton(Settings)

        self.horizontalLayout_4.addWidget(self.themeDefault)

        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)

        self.lFile = QLabel(Settings)
        self.lFile.setMinimumSize(QSize(218, 0))
        self.lFile.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lFile, 3, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.lAuto = QLabel(Settings)
        self.lAuto.setMaximumSize(QSize(58, 16777215))

        self.horizontalLayout_2.addWidget(self.lAuto)

        self.AutoSave = QCheckBox(Settings)
        self.AutoSave.setMaximumSize(QSize(40, 20))
        icon3 = QIcon(QIcon.fromTheme("document-save"))
        self.AutoSave.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.AutoSave)

        self.Interval = QSpinBox(Settings)
        self.Interval.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.Interval.setMinimum(10)
        self.Interval.setMaximum(99)

        self.horizontalLayout_2.addWidget(self.Interval)

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()

        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 2)

        self.lHot = QLabel(Settings)
        self.lHot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lHot, 6, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.lAdd = QLabel(Settings)

        self.verticalLayout_2.addWidget(self.lAdd)

        self.lDel = QLabel(Settings)

        self.verticalLayout_2.addWidget(self.lDel)

        self.lTop = QLabel(Settings)

        self.verticalLayout_2.addWidget(self.lTop)

        self.gridLayout.addLayout(self.verticalLayout_2, 7, 0, 3, 1)

        self.KeyAdd = QKeySequenceEdit(Settings)

        self.gridLayout.addWidget(self.KeyAdd, 7, 1, 1, 1)

        self.KeyDelete = QKeySequenceEdit(Settings)

        self.gridLayout.addWidget(self.KeyDelete, 8, 1, 1, 1)

        self.KeyTop = QKeySequenceEdit(Settings)

        self.gridLayout.addWidget(self.KeyTop, 9, 1, 1, 1)

        self.lTranslate = QLabel(Settings)
        self.lTranslate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lTranslate, 10, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.Online = QCheckBox(Settings)
        icon4 = QIcon(QIcon.fromTheme("applications-internet"))
        self.Online.setIcon(icon4)

        self.horizontalLayout.addWidget(self.Online)

        self.LReload = QPushButton(Settings)
        icon5 = QIcon(QIcon.fromTheme("view-refresh"))
        self.LReload.setIcon(icon5)

        self.horizontalLayout.addWidget(self.LReload)

        icon6 = QIcon(QIcon.fromTheme("folder-open"))

        self.viewLexicons = QToolButton(Settings)
        self.viewLexicons.setIcon(icon6)
        self.viewLexicons.setIconSize(QSize(30, 16))

        self.horizontalLayout.addWidget(self.viewLexicons)

        self.gridLayout.addLayout(self.horizontalLayout, 11, 0, 1, 2)

        self.LexiconBox = QGroupBox(Settings)
        self.verticalLayout_3 = QVBoxLayout(self.LexiconBox)
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.Lexicons = QScrollArea(self.LexiconBox)
        self.Lexicons.setFrameShape(QFrame.Shape.NoFrame)
        self.Lexicons.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 401, 64))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
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
