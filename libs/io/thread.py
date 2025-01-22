from PySide6.QtCore import QThread, QTimer

_objects = set()

class Scheduler(QTimer):
    def __init__(self, target, interval=500):
        super().__init__()
        _objects.add(self)
        self.timeout.connect(target)
        self.start(interval)
    
    def stop(self):
        super().stop()
        _objects.remove(self)

class Thread(QThread):
    result = None

    def __init__(self, target, *args):
        super().__init__()
        _objects.add(self)
        self.finished.connect(lambda:_objects.remove(self))
        self._target = target
        self._args = args
        self.start()
    
    def run(self):
        self.result = self._target(*self._args)

class Pool:
    results = []

    def __init__(self):
        self.threads = [] # type: list[Thread]

    def submit(self, task, *args):
        self.threads.append(Thread(task, *args))
    
    def wait(self):
        for t in self.threads:
            t.wait()
            self.results.append(t.result)
