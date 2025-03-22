from zlib import compress, decompress
import pickle


def load(file):
    return pickle.loads(decompress(open(file, "rb").read()))


def dump(file, obj):
    open(file, "wb").write(compress(pickle.dumps(obj)))
