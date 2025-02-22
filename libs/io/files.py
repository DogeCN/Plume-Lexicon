from libs.translate import Result
from libs.io.stdout import print
from .base import load, dump


def readVocabulary(file_name) -> list[Result]:
    print(f"Loading Vocabulary File: '{file_name}'", "Blue")
    try:
        return load(file_name)
    except:
        return []


def saveVocabulary(results: list[Result], file_name):
    try:
        dump(file_name, results)
        print(f"Saved Vocabulary Flie: '{file_name}'", "Green")
    except Exception as e:
        print(f"Failed to Save Vocabulary Flie: {e}", "Red", "Bold")
