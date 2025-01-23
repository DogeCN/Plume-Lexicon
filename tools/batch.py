from .base import *
from ._batch import _export, _import, _update

tool = Tool(1)
tool.name = "Batch"
tool.name_zh = "批量"
tool.action.tools = [_import.tool, _export.tool, _update.tool]
tool.action.icon = "mail-send"
