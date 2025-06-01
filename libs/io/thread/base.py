from PySide6.QtCore import (
    QObject,
    Signal,
    QThread,
    QTimer,
    QRunnable,
    QThreadPool,
    QMutex,
)

manager = QObject()
pool = QThreadPool.globalInstance()


class Mutex(QMutex):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self.lock()

    def __exit__(self, *_):
        self.unlock()


__all__ = [
    "manager",
    "pool",
    "QObject",
    "Signal",
    "QThread",
    "QTimer",
    "QRunnable",
    "QThreadPool",
    "Mutex",
]
