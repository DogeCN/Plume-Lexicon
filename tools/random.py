from .base import *
from random import choice, randint
from libs.translate.lexicons import matcher


def all():
    word = matcher.random()
    if word:
        tool.mw.ui.WordEntry.setText(word)


def inbank():
    Bank = tool.mw.ui.Bank
    items = Bank.items
    if items:
        Bank.current = choice(items)


def choose(dict: dict):
    return list(dict.keys())[randint(0, len(dict) - 1)]


tool1 = Tool()
tool1.name = "Random all"
tool1.name_zh = "随机所有"
tool1.doc = "Random word in dictionary"
tool1.doc_zh = "在字典中随机"
tool1.action.shortcut = "Ctrl+Shift+R"
tool1.entrance = all

tool2 = Tool()
tool2.name = "Random in bank"
tool2.name_zh = "随机单词"
tool2.doc = "Random word in bank"
tool2.doc_zh = "在单词表中随机单词"
tool2.action.shortcut = "Ctrl+Alt+R"
tool2.entrance = inbank

tool = Tool(1)
tool.name = "Random"
tool.name_zh = "随机"
tool.action.tools = [tool1, tool2]
tool.action.icon = "help-browser"
