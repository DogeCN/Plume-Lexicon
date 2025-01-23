from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from libs.configs.settings import Setting

icon = QIcon(QIcon.fromTheme("emblem-synchronized"))


def setupUi(Dialog: QDialog, Tr):
    global Columns, Font, Font_Size, Stamp, Stamp_Format, Word_Count, Word, Informations, Translations
    if not Dialog.objectName():
        Dialog.setObjectName("Dialog")
    Dialog.setWindowIcon(icon)
    Dialog.resize(373, 155)
    gridLayout = QGridLayout(Dialog)
    gridLayout.setObjectName("gridLayout")
    horizontalLayout = QHBoxLayout()
    horizontalLayout.setObjectName("horizontalLayout")
    label = QLabel(Dialog)
    label.setObjectName("label")
    label.setMaximumSize(QSize(50, 16777215))

    horizontalLayout.addWidget(label)

    Columns = QSpinBox(Dialog)
    Columns.setObjectName("Columns")
    Columns.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    Columns.setMinimum(1)
    Columns.setMaximum(6)
    Columns.setValue(4)

    horizontalLayout.addWidget(Columns)

    gridLayout.addLayout(horizontalLayout, 0, 0, 1, 1)

    horizontalLayout_2 = QHBoxLayout()
    horizontalLayout_2.setObjectName("horizontalLayout_2")
    label_2 = QLabel(Dialog)
    label_2.setObjectName("label_2")

    horizontalLayout_2.addWidget(label_2)

    Font = QFontComboBox(Dialog)
    Font.setObjectName("Font")

    horizontalLayout_2.addWidget(Font)

    Font_Size = QSpinBox(Dialog)
    Font_Size.setObjectName("Font_Size")
    Font_Size.setMinimumSize(QSize(91, 0))
    Font_Size.setMinimum(1)
    Font_Size.setMaximum(30)
    Font_Size.setValue(10)

    horizontalLayout_2.addWidget(Font_Size)

    gridLayout.addLayout(horizontalLayout_2, 1, 0, 1, 1)

    horizontalLayout_3 = QHBoxLayout()
    horizontalLayout_3.setObjectName("horizontalLayout_3")
    label_3 = QLabel(Dialog)
    label_3.setObjectName("label_3")
    label_3.setMaximumSize(QSize(37, 16777215))

    horizontalLayout_3.addWidget(label_3)

    Stamp = QCheckBox(Dialog)
    Stamp.setObjectName("Stamp")
    Stamp.setMaximumSize(QSize(16, 16777215))
    Stamp.setChecked(True)

    horizontalLayout_3.addWidget(Stamp)

    Stamp_Format = QComboBox(Dialog)
    Stamp_Format.addItem("%m/%d")
    Stamp_Format.addItem("%Y/%m/%d")
    Stamp_Format.addItem("%m/%d/%Y")
    Stamp_Format.addItem("%m.%d")
    Stamp_Format.addItem("%Y.%m.%d")
    Stamp_Format.addItem("%m.%d.%Y")
    Stamp_Format.setObjectName("Stamp_Format")

    horizontalLayout_3.addWidget(Stamp_Format)

    Word_Count = QCheckBox(Dialog)
    Word_Count.setObjectName("Word_Count")
    Word_Count.setMaximumSize(QSize(100, 16777215))
    Word_Count.setChecked(True)

    horizontalLayout_3.addWidget(Word_Count)

    gridLayout.addLayout(horizontalLayout_3, 2, 0, 1, 1)

    horizontalLayout_4 = QHBoxLayout()
    horizontalLayout_4.setObjectName("horizontalLayout_4")
    label_4 = QLabel(Dialog)
    label_4.setObjectName("label_4")

    horizontalLayout_4.addWidget(label_4)

    Word = QCheckBox(Dialog)
    Word.setObjectName("Word")
    Word.setChecked(True)

    horizontalLayout_4.addWidget(Word)

    Informations = QCheckBox(Dialog)
    Informations.setObjectName("Detail")
    Informations.setChecked(True)

    horizontalLayout_4.addWidget(Informations)

    Translations = QCheckBox(Dialog)
    Translations.setObjectName("Translations")
    Translations.setChecked(True)

    horizontalLayout_4.addWidget(Translations)

    gridLayout.addLayout(horizontalLayout_4, 3, 0, 1, 1)

    buttonBox = QDialogButtonBox(Dialog)
    buttonBox.setObjectName("buttonBox")
    buttonBox.setStandardButtons(
        QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
    )

    gridLayout.addWidget(buttonBox, 4, 0, 1, 1)

    buttonBox.accepted.connect(Dialog.accept)
    buttonBox.rejected.connect(Dialog.reject)

    Stamp_Format.setCurrentIndex(0)

    translate = lambda key: Setting.translateUI(key, Tr)
    label.setText(translate("Columns"))
    label_2.setText(translate("Font"))
    Font_Size.setSuffix(translate("Pt"))
    label_3.setText(translate("Stamp"))
    label_4.setText(translate("Sections"))
    Word_Count.setText(translate("Word Count"))
    Word.setText(translate("Words"))
    Informations.setText(translate("Phonetic"))
    Translations.setText(translate("Translations"))
