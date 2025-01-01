from .base import *
from ._batch import _export, _import

tool = Tool(1)
tool.name = 'Batch'
tool.name_zh = '批量'
tool.action.tools = [_import.tool, _export.tool]
tool.action.icon = 'mail-send'
