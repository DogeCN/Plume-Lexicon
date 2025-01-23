from PySide6.QtCore import QThread, QTimer


class Objects(set["Scheduler|Thread"]):

    def clear(self):
        for obj in self:
            self.remove(obj)

    @property
    def names(self):
        return [obj.name for obj in self]


_objects = Objects()


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

    @property
    def name(self):
        return self._target.__name__


class Thread(QThread):
    result = None

    def __init__(self, target, *args):
        super().__init__()
        _objects.add(self)
        self.finished.connect(self.remove)
        self._target = target
        self._args = args
        self.start()

    def run(self):
        self.result = self._target(*self._args)

    def remove(self):
        print(self._target.__name__, "finished")
        _objects.remove(self)
        name = self.name
        print(f"{name} count: {_objects.names.count(name)}")

    @property
    def name(self):
        return self._target.__name__


class Pool:
    def __init__(self):
        self.results = []
        self.threads = []  # type: list[Thread]

    def submit(self, task, *args):
        self.threads.append(Thread(task, *args))

    def wait(self):
        for t in self.threads:
            t.wait()
            self.results.append(t.result)
