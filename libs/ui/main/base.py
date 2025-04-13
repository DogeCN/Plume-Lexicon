from PySide6 import QtWidgets, QtCore, QtGui
from libs.debris import GetNewFileName, Explore
from libs.translate import Result
from libs.configs import *
from libs.io import files
from libs.io.stdout import print
import info, pickle

from libs.ui import Dialog

TOP = QtWidgets.QAbstractItemView.ScrollHint.PositionAtTop


class BaseListWidget(QtWidgets.QListWidget):

    def update(self):
        st = self.statusTip()
        r = st.split()[0] if st else ""
        n = self.count()
        self.setStatusTip(f"{r} ({n})" if n > 0 else r)

    def addItem(self, item):
        super().addItem(item)
        self.update()

    def clear(self):
        self.selectionModel().clear()
        super().clear()
        self.update()


class BaseListWidgetItem(QtWidgets.QListWidgetItem): ...


class LItem(BaseListWidgetItem):
    def __init__(self, result: Result):
        super().__init__(result.word)
        self.result = result
        self.word = result.word
        self.setToolTip(result.getTranslation())
        self.setBackground(
            self.dcolor(*info.item_tbg)
            if result.online
            else self.dcolor(*info.item_obg)
        )
        self.update()

    @property
    def top(self):
        return self.result.top

    @top.setter
    def top(self, value):
        self.result.top = value
        self.update()

    def dcolor(self, r, g, b):
        return QtGui.QColor(r, g, b, info.fade(self.result.past))

    def update(self):
        self.setText("*" + self.word if self.top else self.word)

    def __str__(self):
        return self.result.getTranslation()


class Bank(BaseListWidget):
    onEdit = QtCore.Signal()
    menu = None

    def initMenu(self):
        self.menu = QtWidgets.QMenu(self)

        copy = QtGui.QAction(Setting.translateUI("Copy"), self)
        copy.setShortcut("Ctrl+C")
        copy.setIcon(QtGui.QIcon.fromTheme("edit-copy"))
        copy.triggered.connect(self.copy)
        self.menu.addAction(copy)

        cut = QtGui.QAction(Setting.translateUI("Cut"), self)
        cut.setShortcut("Ctrl+X")
        cut.setIcon(QtGui.QIcon.fromTheme("edit-cut"))
        cut.triggered.connect(self.cut)
        self.menu.addAction(cut)

        paste = QtGui.QAction(Setting.translateUI("Paste"), self)
        paste.setShortcut("Ctrl+V")
        paste.setIcon(QtGui.QIcon.fromTheme("edit-paste"))
        paste.triggered.connect(self.paste)
        self.menu.addAction(paste)

        self.menu.addSeparator()

        selectAll = QtGui.QAction(Setting.translateUI("Select All"), self)
        selectAll.setShortcut("Ctrl+A")
        selectAll.setIcon(QtGui.QIcon.fromTheme("edit-select-all"))
        selectAll.triggered.connect(self.selectAll)
        self.menu.addAction(selectAll)

        deselect = QtGui.QAction(Setting.translateUI("Deselect"), self)
        deselect.triggered.connect(self.clearSelection)
        deselect.setIcon(QtGui.QIcon.fromTheme("edit-clear"))
        self.menu.addAction(deselect)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda p: self.menu.exec(self.mapToGlobal(p))
        )

    def keyPressEvent(self, event):
        if self.menu:
            if event.matches(QtGui.QKeySequence.StandardKey.Copy):
                self.copy()
            elif event.matches(QtGui.QKeySequence.StandardKey.Cut):
                self.cut()
            elif event.matches(QtGui.QKeySequence.StandardKey.Paste):
                self.paste()
            else:
                super().keyPressEvent(event)

    def copy(self):
        try:
            items = self.selections
            if items:
                datas = [pickle.dumps(item.result) for item in items]
                mime = QtCore.QMimeData()
                mime.setData(info.mime, pickle.dumps(datas))
                info.clipboard.setMimeData(mime)
        except Exception as e:
            print(f"Copy Failed: {e}", "Red")

    def cut(self):
        self.copy()
        self.remove()

    def paste(self):
        try:
            mime = info.clipboard.mimeData()
            if mime.hasFormat(info.mime):
                datas = pickle.loads(mime.data(info.mime))
                for data in datas:
                    self.append(pickle.loads(data))
        except Exception as e:
            print(f"Paste Failed: {e}", "Red")

    def top(self):
        for item in self.selections:
            item.top = not item.top
        self.onEdit.emit()
        self.roll()

    def append(self, result: Result | list[Result]):
        if isinstance(result, list):
            for r in result:
                self.append(r)
            self.scrollToTop()
        else:
            if result in self.results:
                self.roll(result.word)
                return
            item = LItem(result)
            self.addItem(item)
            self.scrollToItem(item, TOP)
            self.onEdit.emit()

    def roll(self, word: str = None):
        if word:
            word = word.lower()
            for i in self.items:
                if i.word.startswith(word) and not i.result.top:
                    self.scrollToItem(i, TOP)
                    return
        self.scrollToItem(self.current, TOP)

    def remove(self):
        for item in self.selections:
            row = self.row(item)
            self.takeItem(row)
        self.onEdit.emit()
        self.update()

    @property
    def items(self) -> list[LItem]:
        return [self.item(i) for i in range(self.count())]

    @items.setter
    def items(self, items: LItem):
        self.clear()
        for i in items:
            self.addItem(i)

    @property
    def selections(self) -> list[LItem]:
        return self.selectedItems()

    @property
    def current(self) -> LItem:
        return self.currentItem()

    @current.setter
    def current(self, item: LItem):
        self.setCurrentItem(item)
        self.scrollToItem(item, TOP)

    @property
    def results(self):
        return [i.result for i in self.items]

    @results.setter
    def results(self, results):
        if results != self.results:
            self.items = [LItem(i) for i in results]

    @property
    def words(self):
        return [i.word for i in self.items]


class FItem(BaseListWidgetItem):
    _results = []
    origin = []
    loaded = False
    _saved = True
    _file = ""
    _name = ""

    def __init__(self, file: str):
        super().__init__()
        self.file = info.os.path.abspath(file)
        self.setBackground(QtGui.QColor(*info.item_fbg))

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file: str):
        self._file = file.replace("\\", "/")
        self.name = self.file.split("/")[-1]
        self.setToolTip(self.file)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.setText(name)

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        if results != self._results:
            self._results = results
        self.saved = self.origin == results

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, value):
        self.setText(self.name if value else "*" + self.name)
        if value and self.exists():
            self.origin = self.results[:]
            self.joinRecent()
        self._saved = value

    def exists(self, file=None):
        return info.os.path.exists(file if file else self.file)

    def load(self):
        if self.exists():
            self.results = files.readVocabulary(self.file)
            self.saved = True
        else:
            self.results = []
        self.loaded = True

    def save(self, silent=False):
        if self.loaded:
            if self.exists():
                files.saveVocabulary(self.results, self.file)
                self.saved = True
            else:
                if not silent:
                    self.saveAs(self.file)

    def saveAs(self, file=None):
        if file:
            file = Dialog.SaveFile(
                None, Setting.getTr("save_as"), info.ext_all_voca, file
            )
            if not file:
                return
            self.file = file
            self.saved = True
        else:
            file = Dialog.SaveFile(None, Setting.getTr("save_as"), info.ext_all_voca)
            if not file:
                return
        files.saveVocabulary(self.results, file)

    def joinRecent(self):
        recent = Publics["recent"]  # type: list
        if self.file in recent:
            recent.remove(self.file)
        recent.insert(0, self.file)
        if len(recent) > info.max_recent:
            recent.pop()
        Publics.dump()


class Files(BaseListWidget):
    displayChanged = QtCore.Signal()

    def __init__(self, parent, bank: Bank):
        super().__init__(parent)
        self.bank = bank
        self.menu = QtWidgets.QMenu(self)
        self.explorer = QtGui.QAction(self.menu)
        self.explorer.setIcon(QtGui.QIcon(QtGui.QIcon.fromTheme("folder-open")))
        self.explorer.triggered.connect(lambda: Explore(self.current.file))
        self.menu.addAction(self.explorer)
        self.menu.addSeparator()
        bank.onEdit.connect(self.keep)
        self.dragMoveEvent = self.handleEvent
        self.itemSelectionChanged.connect(self.display)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

    def showMenu(self, pos):
        self.explorer.setText(Setting.getTr("explore"))
        self.menu.exec(self.mapToGlobal(pos))

    def open(self):
        f = Dialog.OpenFiles(self.parent(), Setting.getTr("load"), info.ext_all_voca)
        if f:
            self.loads(*f)

    def save(self):
        self.current.save()

    def saveAs(self):
        self.current.saveAs()

    def saveAll(self, silent=False):
        for item in self.items:
            item.save(silent)

    def reload(self):
        item = self.current
        if item:
            item.load()
            self.display(item)

    def display(self, item=None):
        item = item if item else self.current
        if item:
            if not item.loaded:
                item.load()
            self.bank.results = item.results
        else:
            self.bank.results = []
        self.displayChanged.emit()

    def loads(self, *file: str, index=0):
        self.current = [self.loadFile(f) for f in file if f.endswith(info.ext_voca)][
            index
        ]

    def loadFile(self, file: str):
        file = info.os.path.abspath(file).replace("\\", "/")
        for item in self.items:
            if item.file == file:
                return item
        item = FItem(file)
        self.addItem(item)
        return item

    def remove(self):
        self.takeItem(self.row(self.current))
        self.update()

    def keep(self):
        if self.current:
            self.current.results = self.bank.results

    def new(self):
        item = FItem(GetNewFileName("untitled", info.ext_voca, self.names))
        self.addItem(item)
        self.current = item

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                if not url.toLocalFile().endswith(info.ext_voca):
                    event.ignore()
                    return
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if self.handleEvent(event):
            self.loads(*(url.toLocalFile() for url in event.mimeData().urls()))

    def handleEvent(self, event: QtGui.QDropEvent):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            return True
        event.ignore()

    @property
    def items(self) -> list[FItem]:
        return [self.item(i) for i in range(self.count())]

    @property
    def files(self):
        return [i.file for i in self.items]

    @property
    def names(self):
        return [i.name for i in self.items]

    @property
    def current(self) -> FItem:
        select = self.selectedItems()
        return select[0] if select else self.currentItem()

    @current.setter
    def current(self, item: FItem):
        self.setCurrentItem(item)
        item.setSelected(True)

    def clear(self):
        super().clear()
        self.bank.clear()
