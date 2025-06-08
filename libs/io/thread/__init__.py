from .base import *


class Scheduler(QTimer):

    def __init__(self, slot: callable, interval=500):
        super().__init__()
        self.moveToThread(manager.thread())
        self.setParent(manager)
        self.timeout.connect(slot)
        self.start(interval)


class Thread(QThread):

    def __init__(self, slot: callable, *args):
        super().__init__()
        self.moveToThread(manager.thread())
        self.setParent(manager)
        self._slot = slot
        self._args = args
        self.start()

    def run(self):
        self._result = self._slot(*self._args)

    def wait(self):
        super().wait()
        return self._result


class Worker(QRunnable):
    def __init__(self, slot: callable, *args):
        super().__init__()
        self._slot = slot
        self._args = args
        self._mutex = Mutex()
        pool.start(self)

    def run(self):
        with self._mutex:
            self._result = self._slot(*self._args)

    def wait(self):
        with self._mutex:
            return self._result


class Pool:
    def __init__(self):
        self._threads: list[Worker] = []

    def submit(self, slot: callable, *args):
        self._threads.append(Worker(slot, *args))

    def wait(self):
        results = [t.wait() for t in self._threads]
        self._threads.clear()
        return results


class QuickSignal(QObject):
    pairs: dict[str, callable] = {}
    trigger = Signal(str, tuple, dict)

    def __init__(self):
        super().__init__()
        self.trigger.connect(self._call)

    def _call(self, name: str, args: tuple, kwargs: dict):
        if name in self.pairs:
            self.pairs[name](*args, **kwargs)
            self.pairs.pop(name)

    def add(self, slot: callable):
        self.pairs[slot.__name__] = slot

    def call(self, name: str, *args, **kwargs):
        self.trigger.emit(name, args, kwargs)


QuickSignal = QuickSignal()
