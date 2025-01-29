# WARNING:
# Extremely UNGRACEFUL :<
# Please DON'T Mimick or LOL.

from .base import *
from PySide6.QtWidgets import QAbstractScrollArea
from PySide6.QtCore import Qt
from libs.io.thread import Pool, Thread, QuickSignal
from libs.io.requests import get
from random import choice
import time

url = "https://apiv3.shanbay.com/weapps/dailyquote/quote/?date=%s"
moons = "🌑🌒🌓🌔🌕🌖🌗🌘"
foods = "🍏🍎🍐🍊🍋🍌🍉🍇🍓🫐🍈🍒🍑🥭🍍"
# Emoji Just for Fun
_flag = True
pool = Pool()


def one(before):
    try:
        day = time.strftime("%Y-%m-%d", time.localtime(time.time() - before * 86400))
        response = get(url % day)
        sentence = response["content"]
        translation = response["translation"]
        result = f"{sentence}\n{translation}"
    except:
        result = tool.tr("no_data")
    return f"{moons[int(day[-1])%8]} {day} {choice(foods)}\n\n{result}"


def main():
    global msg, detail, _flag
    _flag = True
    msg = tool.message._msg(one(0))
    msg.setDetailedText(tool.tr("no_data"))
    detail = msg.buttons()[1]
    _switch()
    detail.clicked.connect(lambda: _switch())
    msg.showEvent = lambda e: msg.adjustPosition(tool.mw)
    msg.exec()


def _switch():
    global _flag
    if _flag:
        detail.setText("More...")
        msg.move(msg.x(), msg.y() + 150)
    else:
        for b in range(1, 10):
            pool.submit(one, b)
        detail.setText("Hide")
        QuickSignal.connect("update", _update)
        Thread(lambda: QuickSignal.emit("update", pool.wait()))
        area: QAbstractScrollArea = msg.findChild(QAbstractScrollArea)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg.move(msg.x(), msg.y() - 150)
        area.setFixedHeight(300)
    _flag = not _flag


def _update(results):
    msg.setDetailedText("\n\n\n".join(results))
    detail.setText("Hide")


tool = Tool()
tool.name = "ONE"
tool.name_zh = "壹句"
tool.doc = "Show today's daily sentence"
tool.doc_zh = "显示每日一句"
tool.action.icon = "emblem-favorite"
tool.tr.Tr = {"no_data": ("没有数据", "No Data")}
tool.entrance = main
