from ..base import *


def main():
    file = tool.dialog.SaveFile(type="*.txt")
    if file:
        open(file, "w", encoding="utf-8").write(
            "\n".join(
                [f"{'*' if r.top else ''}{r.word}" for r in tool.mw.ui.Bank.results]
            )
        )
        tool.dialog.Pop(file) if tool.message.Ask(tool.tr("open") % file) else ...


tool = Tool()
tool.name = "Export"
tool.name_zh = "导出"
tool.doc = "Export words file"
tool.doc_zh = "导出单词"
tool.action.shortcut = "Ctrl+Alt+E"
tool.tr.Tr = {"open": ("是否打开 '%s'", "Open '%s'?")}
tool.entrance = main
