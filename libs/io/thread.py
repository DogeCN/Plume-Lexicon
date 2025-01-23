from PySide6.QtCore import QThread, QTimer


_objects = set()


class Scheduler(QTimer):
    def __init__(self, target, interval=500):
        super().__init__()
        _objects.add(self)
        self._target = target
        self.timeout.connect(target)
        self.start(interval)

    def stop(self):
        super().stop()
        _objects.remove(self)


class Thread(QThread):
    def __init__(self, target, *args):
        super().__init__()
        _objects.add(self)
        self.finished.connect(self.remove)
        self._target = target
        self._args = args
        self.start()

    def run(self):
        self._result = self._target(*self._args)

    def remove(self):
        _objects.remove(self)

    def wait(self):
        super().wait()
        return self._result


class Pool:
    def __init__(self):
        self._threads = []  # type: list[Thread]

    def submit(self, task, *args):
        self._threads.append(Thread(task, *args))

    def wait(self):
        results = [t.wait() for t in self._threads]
        self._threads.clear()
        return results
