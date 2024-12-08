from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.config import Setting

class Ui_Settings(object):
    def setupUi(self, Settings:QDialog):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(520, 430)
        icon = QIcon(QIcon.fromTheme(u"document-properties"))
        Settings.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lLang = QLabel(Settings)
        self.lLang.setObjectName(u"lLang")
        self.lLang.setMaximumSize(QSize(57, 16777215))

        self.horizontalLayout_5.addWidget(self.lLang)

        self.Lang = QComboBox(Settings)
        self.Lang.addItem(u"\u7b80\u4f53\u4e2d\u6587")
        self.Lang.addItem(u"English")
        self.Lang.setObjectName(u"Lang")

        self.horizontalLayout_5.addWidget(self.Lang)


        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 0, 2, 3, 1)

        self.lFile = QLabel(Settings)
        self.lFile.setObjectName(u"lFile")
        self.lFile.setMinimumSize(QSize(218, 0))
        self.lFile.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lFile, 1, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lVoc = QLabel(Settings)
        self.lVoc.setObjectName(u"lVoc")
        self.lVoc.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.lVoc)

        self.Vocabulary = QLineEdit(Settings)
        self.Vocabulary.setObjectName(u"Vocabulary")
        self.Vocabulary.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.Vocabulary)

        self.viewVocabulary = QToolButton(Settings)
        self.viewVocabulary.setObjectName(u"viewVocabulary")
        icon1 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.viewVocabulary.setIcon(icon1)
        self.viewVocabulary.setIconSize(QSize(30, 16))

        self.horizontalLayout_4.addWidget(self.viewVocabulary)


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lAuto = QLabel(Settings)
        self.lAuto.setObjectName(u"lAuto")
        self.lAuto.setMaximumSize(QSize(58, 16777215))

        self.horizontalLayout_3.addWidget(self.lAuto)

        self.Auto_Save = QCheckBox(Settings)
        self.Auto_Save.setObjectName(u"Auto_Save")
        self.Auto_Save.setMaximumSize(QSize(40, 20))
        icon2 = QIcon(QIcon.fromTheme(u"document-save"))
        self.Auto_Save.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.Auto_Save)

        self.Interval = QSpinBox(Settings)
        self.Interval.setObjectName(u"Interval")
        self.Interval.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.Interval.setMinimum(10)
        self.Interval.setMaximum(99)

        self.horizontalLayout_3.addWidget(self.Interval)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)

        self.lHot = QLabel(Settings)
        self.lHot.setObjectName(u"lHot")
        self.lHot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lHot, 4, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lAdd = QLabel(Settings)
        self.lAdd.setObjectName(u"lAdd")

        self.verticalLayout_2.addWidget(self.lAdd)

        self.lDel = QLabel(Settings)
        self.lDel.setObjectName(u"lDel")

        self.verticalLayout_2.addWidget(self.lDel)

        self.lTop = QLabel(Settings)
        self.lTop.setObjectName(u"lTop")

        self.verticalLayout_2.addWidget(self.lTop)


        self.gridLayout.addLayout(self.verticalLayout_2, 5, 0, 3, 1)

        self.Key_Add = QKeySequenceEdit(Settings)
        self.Key_Add.setObjectName(u"Key_Add")

        self.gridLayout.addWidget(self.Key_Add, 5, 1, 1, 1)

        self.Key_Delete = QKeySequenceEdit(Settings)
        self.Key_Delete.setObjectName(u"Key_Delete")

        self.gridLayout.addWidget(self.Key_Delete, 6, 1, 1, 1)

        self.Key_Top = QKeySequenceEdit(Settings)
        self.Key_Top.setObjectName(u"Key_Top")

        self.gridLayout.addWidget(self.Key_Top, 7, 1, 1, 1)

        self.lTranslate = QLabel(Settings)
        self.lTranslate.setObjectName(u"lTranslate")
        self.lTranslate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lTranslate, 8, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Online = QCheckBox(Settings)
        self.Online.setObjectName(u"Online")
        icon3 = QIcon(QIcon.fromTheme(u"applications-internet"))
        self.Online.setIcon(icon3)

        self.horizontalLayout.addWidget(self.Online)

        self.LReload = QPushButton(Settings)
        self.LReload.setObjectName(u"LReload")
        icon4 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.LReload.setIcon(icon4)

        self.horizontalLayout.addWidget(self.LReload)

        self.viewLexicons = QToolButton(Settings)
        self.viewLexicons.setObjectName(u"viewLexicons")
        self.viewLexicons.setIcon(icon1)
        self.viewLexicons.setIconSize(QSize(30, 16))

        self.horizontalLayout.addWidget(self.viewLexicons)


        self.gridLayout.addLayout(self.horizontalLayout, 9, 0, 1, 2)

        self.LexiconBox = QGroupBox(Settings)
        self.LexiconBox.setObjectName(u"LexiconBox")
        self.verticalLayout_3 = QVBoxLayout(self.LexiconBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.Lexicons = QScrollArea(self.LexiconBox)
        self.Lexicons.setObjectName(u"Lexicons")
        self.Lexicons.setFrameShape(QFrame.Shape.NoFrame)
        self.Lexicons.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Lexicons.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Lexicons.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 401, 122))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Lexicons.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.Lexicons)


        self.gridLayout.addWidget(self.LexiconBox, 10, 0, 1, 2)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)


    def retranslateUi(self, Settings:QDialog):
        Settings.setWindowTitle(Setting.translateUI('Settings'))
        self.lLang.setText(Setting.translateUI('Language'))
        self.lFile.setText(Setting.translateUI('Files'))
        self.lVoc.setText(Setting.translateUI('Vocabulary'))
        self.lAuto.setText(Setting.translateUI('Auto Save'))
        self.Interval.setSuffix(Setting.translateUI(' Secs'))
        self.lAdd.setText(Setting.translateUI('Add'))
        self.lDel.setText(Setting.translateUI('Delete'))
        self.lTop.setText(Setting.translateUI('Top'))
        self.Online.setText(Setting.translateUI('Online'))
        self.LReload.setText(Setting.translateUI('Reload Lexicons'))
        self.LexiconBox.setTitle(Setting.translateUI('Lexicons'))
        self.lHot.setText(Setting.translateUI('Hotkeys'))
        self.lTranslate.setText(Setting.translateUI('Translate'))

