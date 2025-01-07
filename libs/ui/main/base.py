from PySide6 import QtWidgets, QtCore, QtGui
from libs.debris import Get_New_File_Name
from libs.translate import Result
from libs.configs.settings import Setting
from libs.io import io, dialog
from math import log10
import info

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

    def top(self):
        for item in self.selections:
            item.top = not item.top
        self.scrollToItem(self.current, TOP)

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

    def roll(self, word:str):
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
    _results = None
    _saved = True
    _file = ''
    _name = ''
    on_display = False

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
        self._results = results
    
    @property
    def saved(self):
        return self._saved
    
    @saved.setter
    def saved(self, value):
        self.setText(self.name if value else '*'+self.name)
        self._saved = value

    def exists(self, file=None):
        return info.os.path.exists(file if file else self.file)

    def load(self):
        if self.exists():
            self.results = io.read_vocabulary(self.file)
        else: self.results = []
    
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

class Files(BaseListWidget):

    def __init__(self, parent, bank:Bank):
        super().__init__(parent)
        self.bank = bank

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
        if not self.current:
            self.bank.clear()
        self.update()

    def keep(self):
        self.current.results = self.bank.results
        self.current.saved = False

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

    def clear(self):
        super().clear()
        self.bank.clear()


