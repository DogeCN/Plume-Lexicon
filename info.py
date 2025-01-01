import os, sys

def check_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

prog_name = 'Plume Lexicon'
prog_name_cn = '羽词'
author = 'DogeCN'
version = 'v1.14.9'
argv0 = sys.argv[0]
argv1 = sys.argv[1] if len(sys.argv) > 1 else None
prog_running = True
data_dir = check_dir(os.getenv('AppData') + os.sep + prog_name + os.sep)
temp_dir = check_dir(os.getenv('Temp') + os.sep + prog_name + os.sep)
cache_dir = check_dir(temp_dir + 'cache' + os.sep)
lexis_dir_name = 'lexicons'
lexis_dir = check_dir(data_dir + lexis_dir_name  + os.sep)
ext_lexi = '.plf'
ext_disabled = '.disabled'
ext_voca = '.pvf'
ext_settings = '.psf'
ext_all_voca = '*' + ext_voca
ext_self_exe = '.exe'
debug_file = data_dir + '.DEBUG'
debug = os.path.exists(debug_file)
temp = temp_dir + 'temp'
timeout = 3
running = data_dir + '.running'
running_sign = ' '
tools = 'tools'
default_voca = data_dir + 'vocabulary' + ext_voca
reg_ext = 'Software\\Classes\\' + ext_voca
reg_cmd = 'shell\\open\\command'
repo_name = 'Plume-Lexicon'
repo_url = f'github.com/{author}/{repo_name}'
url_trans = 'https://trans-api.dogecn.workers.dev/translate_a/single?client=gtx&dt=t&sl=auto&tl=%s&q=%s'
htip_hint = '<html><body><p><span style=" font-size:11pt; font-weight:600;">%s</span style=" font-size:10pt"></p><p>%s</p></body></html>'
speech_hint = '<html><body style=" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; "><p>%s</p></body></html>'
log = data_dir + 'latest.log'
settings = data_dir + 'settings' + ext_settings
public = data_dir + 'public.json'
nontr = ('暂无翻译', 'None Translations')
lurl = f'https://raw.githubusercontent.com/{author}/{repo_name}/refs/heads/main/{lexis_dir_name}/%s'
lurl_cn = 'https://ghproxy.cn/' + lurl

default_lexis = ['Base', 'Long', 'Phrase', 'Term']
seps = [' ', '-']

Tr = {
    'title' : (prog_name_cn, prog_name),
    'load' : ('载入单词表', 'Load Vocubulary File'),
    'save_as' : ('保存单词表', 'Save Vocubulary File'),
    'warning' : ('警告', 'Warning'),
    'unload' : ('未加载', 'Unload'),
    'loadfailed' : ('加载失败', 'Failed to Load'),
    'translate_function_unavailable' : (
        '''无法加载词典
翻译功能不可用
但你可以浏览已有词汇
(首次使用需连接互联网)''',
        '''Can't load lexicons.
Although the translate function is unavailable,
you can read existed vocabularies.
(Internet connection required for the first use)'''
        ),
    'correct_hint' : ('双击更正', 'Double Click to Correct'),
    'speech_hint' : ('双击朗读', 'Double Click to Speech Out'),
    'default_file' : ('选择默认单词表', 'Choose The Default Vocabulary File'),
    'htip' : ('你是否在找 %s: ', 'Do you mean %s: '),
}

StlSheets = {
    'tmenu' : 'border-radius:5px;',
    'raw' : 'background-color: rgb(30, 30, 30);',
    'green' : 'color: rgb(30,200,30);',
    'red' : 'color: rgb(200,30,30);'
}

UITr = {
    'Setting' : '设置',
    'Language' : '语言',
    'Auto Save' : '自动保存',
    'Top' : '置顶',
    'Files' : '文件',
    'Delete' : '删除',
    'Vocabulary' : '词汇表',
    'Secs' : '秒',
    'Add' : '添加',
    'Hotkeys' : '快捷键',
    'Translate' : '翻译',
    'Word Entry' : '输入框',
    'Enter a word' : '请输入单词',
    'Add into Vocabulary' : '加入单词表',
    'Vocabulary Bank' : '词汇表',
    'Translations' : '翻译',
    'Top the Words' : '置顶单词',
    'Delete the Words' : '删除已选单词',
    'Exchanges' : '变形',
    'Phonetic' : '音标',
    'Expand' : '扩展',
    'File' : '文件',
    'Tools' : '工具',
    'Settings' : '设置',
    'About' : '关于',
    'Lexicons' : '词典',
    'Reload' : '重载',
    'Reload Lexicons' : '重载词典',
    'Reload File' : '重载文件',
    'Save' : '保存',
    'Save File' : '保存文件',
    'Load' : '载入',
    'Load Files' : '加载文件',
    'Save As' : '另存为',
    'Save File As ...' : '另存为...',
    'Clear' : '清除',
    'Clear Files' : '清除所有文件',
    'Exit' : '退出',
    'About This Programm' : '关于本项目',
    'About Qt' : '关于Qt',
    'About Qt Engine' : '关于Qt引擎',
    'Relaod Tools' : '重载工具',
    'Remove' : '移除',
    'Remove Current File' : '移除当前文件',
    'New' : '新建',
    'Create a New File' : '新建文件',
    'Save All' : '全部保存',
    'Save All Files' : '保存所有文件',
    'Online' : '在线'
}
