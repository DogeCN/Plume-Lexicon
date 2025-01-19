import pickle, info
from zlib import compress, decompress
from hashlib import md5

def hash_(b) -> str:
    return info.cache_dir + md5(b, usedforsecurity=False).hexdigest()

def load_(file):
    return pickle.load(open(file, 'rb'))

def load(file):
    content = open(file, 'rb').read()
    hash = hash_(content)
    if not info.os.path.exists(hash):
        open(hash, 'wb').write(decompress(content))
    return load_(hash)

def dump_(file, obj):
    pickle.dump(obj, open(file, 'wb'))

def dump(file, obj):
    open(file, 'wb').write(compress(pickle.dumps(obj)))
