from .base import *

def main(*args):
    ui = tool.ui.ui
    results = ui.Bank.results[:]
    for item in ui.Files.items:
        if item != ui.Files.current:
            ui.Bank.append(item.results)
    if results != ui.Bank.results:
        ui.Files.keep()

tool = Tool()
tool.name = 'Mix'
tool.name_zh = '混合'
tool.doc = 'Mix all loaded files as current'
tool.doc_zh = '将所有加载的文件加入当前单词表'
tool.entrance = main
tool.attr = 'Yellow', 'Bold'