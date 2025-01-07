from difflib import SequenceMatcher
from .api import api_translate
from .dict import lexicons
from libs.configs.settings import Setting
import info, time

class Result:
    top = False
    match = False
    online = False

    def __init__(self, word:str='', value:list[str, list[str]]=[*['']*3, []]):
        self.time = time.time()
        self.word = word
        self.value = value

    @property
    def past(self):
        return (time.time() - self.time) / 86400

    @property
    def translation(self):
        translation = self.value[2]
        return translation if translation else info.nontr[0]
    
    @translation.setter
    def translation(self, translation):
        self.value[2] = translation

    def get_translation(self):
        return self.definition if Setting.Language else self.translation

    @property
    def definition(self):
        definition = self.value[1]
        return definition if definition else info.nontr[1]

    @definition.setter
    def definition(self, definition):
        self.value[1] = definition

    def get_definition(self):
        return self.translation if Setting.Language else self.definition

    @property
    def exchanges(self):
        for form in self.value[3]:
            result = translate(form)
            if result:
                yield result

    def _expands(self, sep):
        if sep in self.word:
            for wp in set(self.word.split(sep)):
                result = translate(wp)
                if result:
                    yield result
        for lexicon in lexicons:
            if not lexicon.enabled: continue
            for wp in lexicon:
                if (sep in self.word and self.word != wp and self.word in wp) \
                    or (sep in wp and self.word in wp.split(sep)):
                    yield Result(wp, lexicon[wp])

    @property
    def expands(self):
        for sep in info.seps:
            for result in self._expands(sep):
                yield result

    @property
    def phonetic(self):
        return self.value[0]
    
    def __bool__(self):
        return bool(self.value[1 if Setting.Language else 2]) and not self.match
    
    def __eq__(self, value):
        return self.word == value
    
    def get_tip(self):
        trans_html = self.get_translation().replace('\n', '<br>')
        return info.htip_hint % (Setting.getTr('htip') % self.word, trans_html)

def fast(func):
    def wrapper(word: str, *res_lists: list[Result]) -> Result:
        for res_list in res_lists:
            for res in res_list:
                if res == word:
                    return res
        return func(word)
    return wrapper

@fast
def online_translate(word: str) -> Result:
    result = Result(word)
    try: result.translation = api_translate(word, 0)
    except: ...
    else: result.online = True
    return result

@fast
def translate(word: str) -> Result:
    if word:
        max = 0.3
        s = SequenceMatcher()
        s.set_seq2(word)
        result = None
        for lexicon in lexicons:
            if not lexicon.enabled: continue
            for wp in [word, word.lower(), word.capitalize()]:
                if wp in lexicon:
                    return Result(word, lexicon[wp])

            for wm in lexicon:
                if wm[0] == word[0]:
                    s.set_seq1(wm)
                    if s.real_quick_ratio() > max and s.quick_ratio() > max:
                        ratio = s.ratio()
                        if ratio > max:
                            result = Result(wm, lexicon[wm])
                            max = ratio

        if result is not None:
            result.match = True
            return result
        
    return Result(word)

def trans(word: str, *res_lists):
    if Setting.Online:
        return online_translate(word, *res_lists)
    else:
        return translate(word, *res_lists)
