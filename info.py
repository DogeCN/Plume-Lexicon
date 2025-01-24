from PySide6.QtWidgets import QApplication
from math import log10
import os, sys


def check_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir


prog_name = "Plume Lexicon"
prog_name_cn = "羽词"
author = "DogeCN"
version = "v1.15.1"
app = QApplication()
clipboard = app.clipboard()
argv0 = sys.argv[0]
argv1 = sys.argv[1] if len(sys.argv) > 1 else None
exe = argv0.endswith(".exe")
prog_running = True
data_dir = check_dir(os.getenv("AppData") + os.sep + prog_name + os.sep)
temp_dir = check_dir(os.getenv("Temp") + os.sep + prog_name + os.sep)
cache_dir = check_dir(temp_dir + "cache" + os.sep)
lexis_dir_name = "lexicons"
lexis_dir = check_dir(data_dir + lexis_dir_name + os.sep)
ext_lexi = ".plf"
ext_disabled = ".disabled"
ext_voca = ".pvf"
ext_settings = ".psf"
ext_all_voca = "*" + ext_voca
temp = temp_dir + "temp"
max_recent = 5
min_similarity = 0.5
item_tbg = (255, 100, 100)
item_obg = (100, 255, 255)
item_fbg = (255, 100, 255, 30)
fading_method = lambda c: round(max(255 - log10(c + 1) * 100, 1) / 5)
running = temp_dir + ".running"
running_sign = " "
tools = "tools"
default_voca = data_dir + "default" + ext_voca
reg_ext = "Software\\Classes\\" + ext_voca
reg_cmd = "shell\\open\\command"
cmd = f'"{os.path.abspath(argv0)}" "%1"'
repo_name = "Plume-Lexicon"
repo_url = f"https://github.com/{author}/{repo_name}"
release_api = f"https://api.github.com/repos/{author}/{repo_name}/releases/latest"
url_trans = "https://trans-api.dogecn.workers.dev/translate_a/single?client=gtx&dt=t&sl=auto&tl=%s&q=%s"
htip_hint = '<html><body><p><span style=" font-size:11pt; font-weight:600;">%s</span style=" font-size:10pt"></p><p>%s</p></body></html>'
speech_hint = "<html><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; \"><p>%s</p></body></html>"
log = data_dir + "latest.log"
settings = data_dir + "settings" + ext_settings
public = data_dir + "public.json"
nontr = ("暂无翻译", "None Translations")
lurl = f"https://raw.githubusercontent.com/{author}/{repo_name}/refs/heads/main/{lexis_dir_name}/%s"
lurl_cn = "https://ghproxy.cn/" + lurl

default_lexis = {"Base", "Long", "Phrase", "Term"}
seps = {" ", "-"}

Tr = {
    "title": (prog_name_cn, prog_name),
    "load": ("载入单词表", "Load Vocubulary File"),
    "save_as": ("保存单词表", "Save Vocubulary File"),
    "explore": ("浏览", "Explore"),
    "info": ("信息", "Information"),
    "warning": ("警告", "Warning"),
    "unload": ("未加载", "Unload"),
    "load_failed": ("加载失败", "Failed to Load"),
    "down_failed": (
        """词典下载失败: %s
请检查网络连接""",
        """Failed to download lexicons: %s
Please check your Internet connection""",
    ),
    "lexi_unavailable": (
        """无法加载词典
但你可以浏览已有词汇
(首次使用需连接互联网)""",
        """Can't load lexicons.
You can read existed vocabularies though.
(Internet connection required for the first use)""",
    ),
    "correct_hint": ("双击更正", "Double Click to Correct"),
    "speech_hint": ("双击朗读", "Double Click to Speech Out"),
    "update_tip": ("发现新版本 %s, 是否查看?", "New Version %s Found, Have a Look?"),
    "update_latest": ("已是最新版本", "Already the Latest Version"),
    "update_failed": ("检查更新失败", "Failed to Check Update"),
    "htip": ("你是否在找 %s: ", "Do you mean %s: "),
    "cache_cleared": ("已清除 %s 缓存", "A total of %s caches cleared"),
}

StlSheets = {
    "green": "color: rgb(30,200,30);",
    "red": "color: rgb(200,30,30);",
}

UITr = {
    "Setting": "设置",
    "Interface": "界面",
    "Theme": "主题",
    "Acrylic": "亚克力",
    "Dark": "暗黑",
    "Default": "默认",
    "Language": "语言",
    "Auto Save": "自动保存",
    "Top": "置顶",
    "Files": "文件",
    "Cache": "缓存",
    "Delete": "删除",
    "Vocabulary": "词汇表",
    "Copy": "复制",
    "Paste": "粘贴",
    "Cut": "剪切",
    "Undo": "撤销",
    "Redo": "重做",
    "Select All": "全选",
    "Deselect": "取消选择",
    "Secs": "秒",
    "Add": "添加",
    "Hotkeys": "快捷键",
    "Translate": "翻译",
    "Word Entry": "输入框",
    "Enter a word": "请输入单词",
    "Add into Vocabulary": "加入单词表",
    "Vocabulary Bank": "词汇表",
    "Translations": "翻译",
    "Top the Words": "置顶单词",
    "Delete the Words": "删除已选单词",
    "Exchanges": "变形",
    "Phonetic": "音标",
    "Expand": "扩展",
    "File": "文件",
    "Tools": "工具",
    "Settings": "设置",
    "About": "关于",
    "Lexicons": "词典",
    "Reload": "重载",
    "Reload Lexicons": "重载词典",
    "Reload File": "重载文件",
    "Save": "保存",
    "Save File": "保存文件",
    "Load": "载入",
    "Load Files": "加载文件",
    "Save As": "另存为",
    "Save File As ...": "另存为...",
    "Clear": "清除",
    "Clear Files": "清除所有文件",
    "Clear Recent Records": "清除最近记录",
    "Exit": "退出",
    "About This Programm": "关于本项目",
    "About Qt": "关于Qt",
    "About Qt Engine": "关于Qt引擎",
    "Remove": "移除",
    "Remove Current File": "移除当前文件",
    "Recent": "最近",
    "New": "新建",
    "Create a New File": "新建文件",
    "Save All": "全部保存",
    "Save All Files": "保存所有文件",
    "Online": "在线",
    "Check Update": "检查更新",
    "Check the Latest Version": "检查最新版本",
}
