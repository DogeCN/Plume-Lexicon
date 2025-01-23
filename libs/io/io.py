from libs.configs.settings import Setting
from libs.translate import Result
from libs.stdout import print
from .base import load, dump


def read_vocabulary(file_name) -> list[Result]:
    print(f"Loading Vocabulary File: '{file_name}'", "Blue")
    try:
        return load(file_name)
    except:
        return []


def save_vocabulary(results: list[Result], file_name):
    try:
        dump(file_name, results)
        print(f"Saved Vocabulary Flie: '{file_name}'", "Green")
    except:
        ...
