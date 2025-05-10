class PyEntry:
    phonetic: str
    definition: str
    translation: str
    exchanges: list[str]

    def __init__(
        self,
        phonetic: str,
        definition: str,
        translation: str,
        exchanges: list[str],
    ): ...

class PyDBCreator:
    def __init__(self, path: str, temp: str): ...
    def insert(self, key: str, value: PyEntry): ...
    def export(self): ...
