import os, pickle, info
from libs.debris import Get_New_File_Name
from zlib import compress, decompress
from hashlib import md5

def _hash(b) -> str:
    return info.cache_dir + md5(b, usedforsecurity=False).hexdigest()

def _load(file):
    return pickle.load(open(file, 'rb'))

def load(file):
    if not os.path.exists(hash := _hash(content := open(file, 'rb').read())):
        open(hash, 'wb').write(decompress(content))
    return _load(hash)

def _dump(file, obj):
    pickle.dump(obj, open(file, 'wb'))

def dump(file, obj):
    _dump(temp := Get_New_File_Name(info.temp), obj)
    open(file, 'wb').write(compress(open(temp, 'rb').read()))
