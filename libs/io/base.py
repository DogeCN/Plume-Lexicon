import pickle, info
from zlib import compress, decompress
from hashlib import md5

def hash_(b) -> str:
    return info.cache_dir + md5(b, usedforsecurity=False).hexdigest()

def load_(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def load(file):
    with open(file, 'rb') as f:
        content = f.read()
    hash = hash_(content)
    if not info.os.path.exists(hash):
        with open(hash, 'wb') as f:
            f.write(decompress(content))
    return load_(hash)

def dump_(file, obj):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)

def dump(file, obj):
    with open(file, 'wb') as f:
        f.write(compress(pickle.dumps(obj)))
