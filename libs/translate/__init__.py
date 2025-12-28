from .api import apiTranslate
from .lexicons import Entry, lexicons, matcher
from libs.configs import Setting
import info, time


class Result:
    top = False
    match = False
    online = False

    def __init__(self, word: str = "", entry: Entry = None):
        self.time = time.time()
        self.word = word
        self.entry = entry if entry else Entry("", "", "", [])

    @property
    def past(self):
        return (time.time() - self.time) / 86400

    @property
    def translation(self):
        translation = self.entry.translation
        return translation if translation else info.nontr[0]

    @translation.setter
    def translation(self, translation):
        self.entry.translation = translation

    def getTranslation(self):
        return self.definition if Setting.Language else self.translation

    @property
    def definition(self):
        definition = self.entry.definition
        return definition if definition else info.nontr[1]

    @definition.setter
    def definition(self, definition):
        self.entry.definition = definition

    def getDefinition(self):
        return self.translation if Setting.Language else self.definition

    @property
    def exchanges(self):
        for form in self.entry.exchanges:
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
                if lexicon.enabled:
                    for wp in lexicon.filter(self.word):
                        yield translate(wp)

    @property
    def phonetic(self):
        return self.entry.phonetic

    def __bool__(self):
        return not self.match

    def __eq__(self, value):
        return value == self.word

    def getTip(self):
        trans_html = self.getTranslation().replace("\n", "<br>")
        return info.htip_hint % (Setting.getTr("htip") % self.word, trans_html)


def onlineTranslate(word: str) -> Result:
    result = Result(word)
    try:
        result.translation = apiTranslate(word, Setting.Language)
        result.online = True
    except:
        ...
    return result


def translate(word: str) -> Result:
    if word:
        for lexicon in lexicons:
            if lexicon.enabled:
                for wp in [word, word.lower(), word.capitalize()]:
                    if wp in lexicon:
                        return Result(word, lexicon[wp])

        wp = matcher.find(word)

        if wp:
            result = translate(wp)
            result.match = True
            return result

    return Result(word)


def trans(word: str, results):
    for res in results:
        if res == word:
            return res
    return onlineTranslate(word) if Setting.Online else translate(word)
