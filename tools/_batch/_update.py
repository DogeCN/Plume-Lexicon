from ..base import *
from libs.translate import translate


def main():
    count = 0
    for result in tool.mw.ui.Bank.results:
        new = translate(result.word)
        if new:
            result.entry = new.entry
            count += 1
    tool.message.Show(tool.tr("updated") % count)


tool = Tool()
tool.name = "Update"
tool.name_zh = "更新"
tool.doc = "Update the translations of words"
tool.doc_zh = "更新单词翻译"
tool.action.shortcut = "Ctrl+Alt+U"
tool.action.icon = "view-refresh"
tool.tr.Tr = {"updated": ("已更新 %s 个单词", "Updated %s words.")}
tool.entrance = main
