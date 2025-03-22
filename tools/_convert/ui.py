from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.configs import Setting

icon = QIcon(QIcon.fromTheme("emblem-synchronized"))


def setupUi(Dialog: QDialog, Tr):
    global Columns, Font, FontSize, Stamp, StampFormat, WordCount, Word, Phonetic, Translations

    Dialog.setWindowIcon(icon)
    Dialog.resize(373, 155)
    gridLayout = QGridLayout(Dialog)
    horizontalLayout = QHBoxLayout()
    label = QLabel(Dialog)
    label.setMaximumSize(QSize(50, 16777215))

    horizontalLayout.addWidget(label)

    Columns = QSpinBox(Dialog)
    Columns.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    Columns.setMinimum(1)
    Columns.setMaximum(6)
    Columns.setValue(4)

    horizontalLayout.addWidget(Columns)

    gridLayout.addLayout(horizontalLayout, 0, 0, 1, 1)

    horizontalLayout_2 = QHBoxLayout()
    label_2 = QLabel(Dialog)

    horizontalLayout_2.addWidget(label_2)

    Font = QFontComboBox(Dialog)

    horizontalLayout_2.addWidget(Font)

    FontSize = QSpinBox(Dialog)
    FontSize.setMinimumSize(QSize(91, 0))
    FontSize.setMinimum(1)
    FontSize.setMaximum(30)
    FontSize.setValue(10)

    horizontalLayout_2.addWidget(FontSize)

    gridLayout.addLayout(horizontalLayout_2, 1, 0, 1, 1)

    horizontalLayout_3 = QHBoxLayout()
    label_3 = QLabel(Dialog)
    label_3.setMaximumSize(QSize(37, 16777215))

    horizontalLayout_3.addWidget(label_3)

    Stamp = QCheckBox(Dialog)
    Stamp.setMaximumSize(QSize(16, 16777215))
    Stamp.setChecked(True)

    horizontalLayout_3.addWidget(Stamp)

    StampFormat = QComboBox(Dialog)
    StampFormat.addItem("%m/%d")
    StampFormat.addItem("%Y/%m/%d")
    StampFormat.addItem("%m/%d/%Y")
    StampFormat.addItem("%m.%d")
    StampFormat.addItem("%Y.%m.%d")
    StampFormat.addItem("%m.%d.%Y")

    horizontalLayout_3.addWidget(StampFormat)

    WordCount = QCheckBox(Dialog)
    WordCount.setMaximumSize(QSize(100, 16777215))
    WordCount.setChecked(True)

    horizontalLayout_3.addWidget(WordCount)

    gridLayout.addLayout(horizontalLayout_3, 2, 0, 1, 1)

    horizontalLayout_4 = QHBoxLayout()
    label_4 = QLabel(Dialog)

    horizontalLayout_4.addWidget(label_4)

    Word = QCheckBox(Dialog)
    Word.setChecked(True)

    horizontalLayout_4.addWidget(Word)

    Phonetic = QCheckBox(Dialog)
    Phonetic.setChecked(True)

    horizontalLayout_4.addWidget(Phonetic)

    Translations = QCheckBox(Dialog)
    Translations.setChecked(True)

    horizontalLayout_4.addWidget(Translations)

    gridLayout.addLayout(horizontalLayout_4, 3, 0, 1, 1)

    buttonBox = QDialogButtonBox(Dialog)
    buttonBox.setStandardButtons(
        QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
    )

    gridLayout.addWidget(buttonBox, 4, 0, 1, 1)

    buttonBox.accepted.connect(Dialog.accept)
    buttonBox.rejected.connect(Dialog.reject)

    StampFormat.setCurrentIndex(0)

    translate = lambda key: Setting.translateUI(key, Tr)
    label.setText(translate("Columns"))
    label_2.setText(translate("Font"))
    FontSize.setSuffix(translate("Pt"))
    label_3.setText(translate("Stamp"))
    label_4.setText(translate("Sections"))
    WordCount.setText(translate("Word Count"))
    Word.setText(translate("Words"))
    Phonetic.setText(translate("Phonetic"))
    Translations.setText(translate("Translations"))
