from PySide6.QtCore import QObject, QThread, QTimer


manager = QObject()


class Scheduler(QTimer):

    def __init__(self, target, interval=500):
        super().__init__()
        self.moveToThread(manager.thread())
        self.setParent(manager)
        self.moveToThread(manager.thread())
        self._target = target
        self.timeout.connect(target)
        self.start(interval)


class Thread(QThread):

    def __init__(self, target, *args):
        super().__init__()
        self.moveToThread(manager.thread())
        self.setParent(manager)
        self._target = target
        self._args = args
        self.start()

    def run(self):
        self._result = self._target(*self._args)

    def wait(self):
        super().wait()
        return self._result


class Pool:
    def __init__(self):
        self._threads: list[Thread] = []

    def submit(self, task, *args):
        self._threads.append(Thread(task, *args))

    def wait(self):
        results = [t.wait() for t in self._threads]
        self._threads.clear()
        return results


class QuickSignal(QObject):
    pairs = {}
    queue: list[tuple] = []

    def __init__(self):
        super().__init__()
        Scheduler(self.manage)

    def manage(self):
        if self.queue:
            for name, args, kwargs in self.queue:
                if name in self.pairs:
                    self.pairs[name](*args, **kwargs)
                    self.pairs.pop(name)
            self.queue.clear()

    def connect(self, name, slot):
        self.pairs[name] = slot

    def emit(self, name, *args, **kwargs):
        self.queue.append((name, args, kwargs))


QuickSignal = QuickSignal()
