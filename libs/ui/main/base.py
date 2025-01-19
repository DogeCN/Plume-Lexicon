from PySide6 import QtWidgets, QtCore, QtGui
from libs.debris import Get_New_File_Name
from libs.translate import Result
from libs.stdout import print
from libs.configs.settings import Setting
from libs.configs.public import Publics
from libs.io import io, dialog
from math import log10
import info, pickle

TOP = QtWidgets.QAbstractItemView.ScrollHint.PositionAtTop

class BaseListWidget(QtWidgets.QListWidget):

    def update(self):
        st = self.statusTip()
        r = st.split()[0] if st else ''
        n = self.count()
        self.setStatusTip(f'{r} ({n})' if n > 0 else r)
    
    def addItem(self, item):
        super().addItem(item)
        self.update()
    
    def clear(self):
        super().clear()

class BaseListWidgetItem(QtWidgets.QListWidgetItem): ...

class LItem(BaseListWidgetItem):
    def __init__(self, result:Result):
        super().__init__(result.word)
        self.result = result
        self.word = result.word
        self.setToolTip(result.get_translation())
        self.setBackground(self.dcolor(255, 100, 100) if result.online else self.dcolor(100, 255, 255))
        self.update()

    @property
    def top(self):
        return self.result.top
    
    @top.setter
    def top(self, value):
        self.result.top = value
        self.update()

    def dcolor(self, r, g, b):
        rate = round(max(255 - log10(self.result.past + 1) * 100, 1) / 5)
        return QtGui.QColor(r, g, b, rate)

    def update(self):
        self.setText('*'+self.word if self.top else self.word)

    def __str__(self):
        return self.result.get_translation()

class Bank(BaseListWidget):
    def __init__(self, parent=None, ccenabled=True):
        super().__init__(parent)
        if ccenabled:
            self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        
        copy = QtGui.QAction(Setting.translateUI('Copy'), self)
        copy.setShortcut('Ctrl+C')
        copy.setIcon(QtGui.QIcon.fromTheme('edit-copy'))
        copy.triggered.connect(self.copy)
        menu.addAction(copy)

        cut = QtGui.QAction(Setting.translateUI('Cut'), self)
        cut.setShortcut('Ctrl+X')
        cut.setIcon(QtGui.QIcon.fromTheme('edit-cut'))
        cut.triggered.connect(self.cut)
        menu.addAction(cut)

        paste = QtGui.QAction(Setting.translateUI('Paste'), self)
        paste.setShortcut('Ctrl+V')
        paste.setIcon(QtGui.QIcon.fromTheme('edit-paste'))
        paste.triggered.connect(self.paste)
        menu.addAction(paste)

        menu.addSeparator()

        select_all = QtGui.QAction(Setting.translateUI('Select All'), self)
        select_all.setShortcut('Ctrl+A')
        select_all.setIcon(QtGui.QIcon.fromTheme('edit-select-all'))
        select_all.triggered.connect(self.selectAll)
        menu.addAction(select_all)

        deselect = QtGui.QAction(Setting.translateUI('Deselect'), self)
        deselect.triggered.connect(self.clearSelection)
        deselect.setIcon(QtGui.QIcon.fromTheme('edit-clear'))
        menu.addAction(deselect)

        menu.exec(self.mapToGlobal(pos))

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.StandardKey.Copy): self.copy()
        elif event.matches(QtGui.QKeySequence.StandardKey.Cut): self.cut()
        elif event.matches(QtGui.QKeySequence.StandardKey.Paste): self.paste()
        else: super().keyPressEvent(event)

    def copy(self):
        try:
            items = self.selections
            if items:
                datas = [pickle.dumps(item.result) for item in items]
                info.clipboard.setText(pickle.dumps(datas).decode('latin1'))
        except Exception as e: print(f'Copy Failed: {e}', 'Red')

    def cut(self):
        self.copy()
        self.remove()

    def paste(self):
        try:
            text = info.clipboard.text()
            if text:
                datas = pickle.loads(text.encode('latin1'))
                for data in datas: self.append(pickle.loads(data))
        except Exception as e: print(f'Paste Failed: {e}', 'Red')

    def top(self):
        for item in self.selections:
            item.top = not item.top
        self.roll()

    def append(self, result:Result|list[Result]):
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

    def roll(self, word:str=None):
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
        self.update()

    def clear(self):
        super().clear()
        self.update()

    @property
    def items(self) -> list[LItem]:
        return [self.item(i) for i in range(self.count())]

    @items.setter
    def items(self, items:LItem):
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
    def current(self, item:LItem):
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
    _file = ''
    _name = ''

    def __init__(self, file:str):
        super().__init__()
        self.file = info.os.path.abspath(file)
        self.setBackground(QtGui.QColor(255, 100, 255, 30))
    
    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, file:str):
        self._file = file.replace('\\', '/')
        self.name = self.file.split('/')[-1]
        self.setToolTip(self.file)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name:str):
        self._name = name
        self.setText(name)

    @property
    def results(self):
        if self._results is None:
            self.load()
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
        self.setText(self.name if value else '*'+self.name)
        if value and self.exists():
            self.origin = self.results[:]
            self.join_recent()
        self._saved = value

    def exists(self, file=None):
        return info.os.path.exists(file if file else self.file)

    def load(self):
        if self.exists():
            self.results = io.read_vocabulary(self.file)
            self.saved = True
        else: self.results = []
        self.loaded = True
    
    def save(self, silent=False):
        if self.exists():
            io.save_vocabulary(self.results, self.file)
            self.saved = True
        else:
            if not silent:
                self.save_as(self.file)
    
    def save_as(self, file=None):
        if file:
            file = dialog.SaveFile(None, Setting.getTr('save_as'), info.ext_all_voca, file)
            if not file: return
            self.file = file
            self.saved = True
        else:
            file = dialog.SaveFile(None, Setting.getTr('save_as'), info.ext_all_voca)
            if not file: return
        io.save_vocabulary(self.results, file)

    def join_recent(self):
        recent = Publics['recent'] #type: list
        if self.file in recent:
            recent.remove(self.file)
        recent.insert(0, self.file)
        if len(recent) > info.max_recent: recent.pop()
        Publics['recent'] = recent

class Files(BaseListWidget):

    def __init__(self, parent, bank:Bank):
        super().__init__(parent)
        self.bank = bank
        self.itemSelectionChanged.connect(self.display_file)
        self.menu = QtWidgets.QMenu(self)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda p:self.menu.exec(self.mapToGlobal(p)))

    def open(self):
        f = dialog.OpenFiles(self.parent(), Setting.getTr('load'), info.ext_all_voca)
        if f: self.display_file(self.load(f)[0])

    def save(self):
        self.current.save()

    def save_as(self):
        self.current.save_as()

    def save_all(self, silent=True):
        for item in self.items: item.save(silent)
    
    def reload(self):
        item = self.current
        if item:
            item.load()
            self.display_file(item)

    def display_file(self, item=None):
        item = item if item else self.current
        if item in self.items:
            if not item.loaded: item.load()
            self.bank.results = item.results

    def load(self, file:str|list[str]):
        if isinstance(file, list):
            return [self.load(f) for f in file]
        else:
            file = info.os.path.abspath(file).replace('\\', '/')
            for item in self.items:
                if item.file == file:
                    item.load()
                    return item
            item = FItem(file)
            self.addItem(item)
            return item

    def remove(self):
        self.takeItem(self.row(self.current))
        self.update()

    def keep(self):
        if self.current: self.current.results = self.bank.results

    def new(self, fn=None):
        if not fn:
            fn = Get_New_File_Name('untitled', info.ext_voca, self.names)
        item = FItem(fn)
        self.addItem(item)
        self.current = item
        return item

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                if not url.toLocalFile().endswith(info.ext_voca):
                    event.ignore()
                    return
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event:QtGui.QDropEvent):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                self.load(url.toLocalFile())
        else:
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
        item = self.currentItem()
        if not item:
            items = self.items
            if items:
                item = items[0]
                self.current = item
        return item
    
    @current.setter
    def current(self, item:FItem):
        self.setCurrentItem(item)
        self.display_file()

    def clear(self):
        super().clear()
        self.bank.clear()


