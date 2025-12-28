from libs.debris import GetLanguage
from libs.io.base import load, dump
from libs.io.stdout import print
import info

data = info.settings


class Settings:
    def __init__(self, file):
        config = {
            "Language": GetLanguage(),
            "Theme": 3,
            "Online": False,
            "AutoSave": True,
            "AutoSaveInterval": 60,
            "KeyAdd": "Ctrl+E",
            "KeyDel": "Del",
            "KeyTop": "Ctrl+T",
        }
        try:
            config.update(load(file).__dict__)
        except:
            ...
        self.__dict__ = config

    def getTr(self, key: str):
        return info.Tr[key][self.Language]

    @staticmethod
    def search(Tr, key: str):
        if key in Tr:
            return Tr[key]
        else:
            sk = key
            for k in Tr:
                if k in key:
                    key = key.replace(k, Tr[k])
            if key != sk:
                return key

    def translateUI(self, key: str, ExTr=None) -> str:
        if self.Language:
            return key
        Tr = info.UITr
        res = self.search(Tr, key)
        if res:
            return res
        if ExTr:
            res = self.search(ExTr, key)
            if res:
                return res
        print(f"Key '{key}' not found", "Yellow", "Bold")
        return key

    @staticmethod
    def load(file=data):
        global Setting
        Setting = Settings(file)

    @staticmethod
    def dump(file=data):
        try:
            dump(file, Setting)
        except:
            ...


Settings.load()
