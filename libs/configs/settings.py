from libs.debris import GetLanguage
from libs.io.base import load, dump
from libs.io.stdout import print
import info

data = info.settings


class Settings:
    def __init__(self, file):
        try:
            self.__dict__ = load(file).__dict__
        except:
            self.Language = GetLanguage()  # 0:zh, 1:en
            self.Theme = 3
            self.Online = False
            self.AutoSave = True
            self.AutoSaveInterval = 60
            self.KeyAdd = "Ctrl+E"
            self.KeyDel = "Del"
            self.KeyTop = "Ctrl+T"

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
