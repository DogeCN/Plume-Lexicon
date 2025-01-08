from ..base import *
from libs.translate import translate

tr = {
    'tip' : ('[请在此处输入单词]', '[Entry Your Words There]'),
    'imported' : ("已导入 '%s'", "Imported '%s'"),
    'corrected' : ('已更正:\n%s', 'Corrected:\n%s'),
    'error' : ('错误: %s', 'Error: %s')
}

def main():
    try:
        files = tool.dialog.OpenFiles(type='*.txt')
        if files:
            results = []
            correct = {}
            for file in files:
                with open(file, 'r', encoding='utf-8') as t:
                    for word in t:
                        word = word.strip()
                        if word:
                            top = word[0] == '*'
                            result = translate(word[1:] if top else word)
                            result.top = top
                            if result.match:
                                correct[word] = result.word
                                result.match = False
                                result.top = True
                            results.append(result)
            tool.mw.ui.Files.new()
            tool.mw.ui.Bank.append(results)
            finfo = ', '.join(files)
            tool.message.Show(tool.tr('imported') % finfo)
            if correct:
                info = '\n'.join([f"'{w}' -> '{correct[w]}'" for w in correct])
                tool.message.Show(tool.tr('corrected') % info)
    except Exception as e:
        tool.message.Error(tool.tr('error') % e)

tool = Tool()
tool.name = 'Import'
tool.name_zh = '导入'
tool.doc = 'Import words file and batch translate to bank'
tool.doc_zh = '导入单词并批量翻译'
tool.action.shortcut = 'Ctrl+Alt+I'
tool.tr.Tr = tr
tool.entrance = main
