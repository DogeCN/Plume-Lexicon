from zlib import compress, decompress
import pickle


def load(file: str) -> object:
    return pickle.loads(decompress(open(file, "rb").read()))


def dump(file: str, obj: object):
    open(file, "wb").write(compress(pickle.dumps(obj)))
