from json import load, dump
import info

data = info.public

class Public(dict):
    def __init__(self, file):
        try:
            self.update(load(open(file, 'r', encoding='utf-8')))
        except:
            self['default_path'] = None
            self['ui_states'] = {}
            self['recent'] = []
            self['debug'] = False
    
    def dump(self):
        try: dump(self, open(data, 'w', encoding='utf-8'), indent=4)
        except: ...

    @staticmethod
    def _load(file=data):
        global Publics
        Publics = Public(file)

    def __setitem__(self, key, value):
        if key in self and self[key] == value:
            return
        super().__setitem__(key, value)
        self.dump()

Public._load()
