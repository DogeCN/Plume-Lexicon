import pickle, info
from zlib import compress, decompress
from hashlib import md5


def hash(b) -> str:
    return info.cache_dir + md5(b, usedforsecurity=False).hexdigest()


def load_(file):
    return pickle.load(open(file, "rb"))


def load(file):
    content = open(file, "rb").read()
    cache = hash(content)
    if not info.os.path.exists(cache):
        open(cache, "wb").write(decompress(content))
    return load_(cache)


def dump_(file, obj):
    pickle.dump(obj, open(file, "wb"))


def dump(file, obj):
    open(file, "wb").write(compress(pickle.dumps(obj)))
