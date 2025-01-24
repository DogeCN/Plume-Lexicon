from .base import *
from PySide6.QtWidgets import QAbstractScrollArea
from PySide6.QtCore import Qt
from libs.io.thread import Pool
from libs.io.requests import get
from random import choice
import time

url = "https://apiv3.shanbay.com/weapps/dailyquote/quote/?date=%s"
moons = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
foods = [
    "🍏",
    "🍎",
    "🍐",
    "🍊",
    "🍋",
    "🍌",
    "🍉",
    "🍇",
    "🍓",
    "🫐",
    "🍈",
    "🍒",
    "🍑",
    "🥭",
    "🍍",
]
# Emoji Just for Fun


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


def main():  # Extremely UNGRACEFUL :<
    global msg, detail
    pool = Pool()
    for b in range(0, 8):
        pool.submit(one, b)
    results = pool.wait()
    msg = tool.message._msg(results[0])
    msg.setDetailedText("\n\n\n".join(results[1:]))
    detail = msg.buttons()[1]
    _switch()
    detail.clicked.connect(lambda: _switch())
    msg.showEvent = lambda e: msg.adjustPosition(tool.mw)
    msg.exec()


_flag = True


def _switch():
    global _flag
    if _flag:
        detail.setText("More...")
        msg.move(msg.x(), msg.y() + 150)
    else:
        detail.setText("Hide")
        area: QAbstractScrollArea = msg.findChild(QAbstractScrollArea)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg.move(msg.x(), msg.y() - 150)
        area.setFixedHeight(300)
    _flag = not _flag


tool = Tool()
tool.name = "ONE"
tool.name_zh = "壹句"
tool.doc = "Show today's daily sentence"
tool.doc_zh = "显示每日一句"
tool.action.icon = "emblem-favorite"
tool.tr.Tr = {"no_data": ("没有数据", "No Data")}
tool.entrance = main
