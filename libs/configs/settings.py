from ..io.base import load, dump
from ..debris import Get_Language
from libs.io.stdout import print
import info

data = info.settings


class Settings:
    def __init__(self, file):
        try:
            self.__dict__ = load(file).__dict__
        except:
            self.Language = Get_Language()  # 0:zh, 1:en
            self.Theme = 3
            self.Online = False
            self.Auto_save = True
            self.Auto_save_interval = 60
            self.Key_Add = "Ctrl+E"
            self.Key_Del = "Del"
            self.Key_Top = "Ctrl+T"

    def getTr(self, key: str):
        return info.Tr[key][self.Language]

    @staticmethod
    def _search(Tr, key: str):
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
        res = self._search(Tr, key)
        if res:
            return res
        if ExTr:
            res = self._search(ExTr, key)
            if res:
                return res
        print(f"Key '{key}' not found", "Yellow", "Bold")
        return key

    @staticmethod
    def _load(file=data):
        global Setting
        Setting = Settings(file)

    @staticmethod
    def dump(file=data):
        try:
            dump(file, Setting)
        except:
            ...


Settings._load()
