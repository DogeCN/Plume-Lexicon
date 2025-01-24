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
