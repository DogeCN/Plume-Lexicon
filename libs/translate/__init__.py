from difflib import SequenceMatcher
from .api import apiTranslate
from .lexicons import lexicons
from libs.configs import Setting
import info, time


class Result:
    top = False
    match = False
    online = False

    def __init__(self, word: str = "", value: list[str, list[str]] = [*[""] * 3, []]):
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

    def getTranslation(self):
        return self.definition if Setting.Language else self.translation

    @property
    def definition(self):
        definition = self.value[1]
        return definition if definition else info.nontr[1]

    @definition.setter
    def definition(self, definition):
        self.value[1] = definition

    def getDefinition(self):
        return self.translation if Setting.Language else self.definition

    @property
    def exchanges(self):
        for form in self.value[3]:
            result = translate(form)
            if result:
                yield result

    @property
    def expands(self):
        for sep in info.seps:
            if sep in self.word:
                for wp in set(self.word.split(sep)):
                    result = translate(wp)
                    if result:
                        yield result
            for lexicon in lexicons:
                if not lexicon.enabled:
                    continue
                for wp in lexicon:
                    if (sep in self.word and self.word != wp and self.word in wp) or (
                        sep in wp and self.word in wp.split(sep)
                    ):
                        yield Result(wp, lexicon[wp])

    @property
    def phonetic(self):
        return self.value[0]

    def __bool__(self):
        return not self.match

    def __eq__(self, value):
        return self.word == value

    def getTip(self):
        trans_html = self.getTranslation().replace("\n", "<br>")
        return info.htip_hint % (Setting.getTr("htip") % self.word, trans_html)


def onlineTranslate(word: str) -> Result:
    result = Result(word)
    try:
        result.translation = apiTranslate(word, Setting.Language)
    except:
        ...
    else:
        result.online = True
    return result


def translate(word: str) -> Result:
    if word:
        for lexicon in lexicons:
            if not lexicon.enabled:
                continue
            for wp in [word, word.lower(), word.capitalize()]:
                if wp in lexicon:
                    return Result(word, lexicon[wp])

        max = info.min_similarity
        s = SequenceMatcher()
        s.set_seq2(word)
        result = None
        for lexicon in lexicons:
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


def trans(word: str, results):
    for res in results:
        if res == word:
            return res
    return onlineTranslate(word) if Setting.Online else translate(word)
