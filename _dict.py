from libs.translate.dict import load
from libs.translate._pickle import Lexicon
from libs.io.base import dump
import info

full = {} #type: Lexicon

ex_b = True

ext = info.ext_lexi
dir = 'lexicons/'
exdir = 'lexicons-extra/'
ex = '-Extra'

lexis = [f'{dir}Base{ext}', f'{dir}Long{ext}', f'{dir}Phrase{ext}', f'{dir}Term{ext}']
lexis_ex = [f'{exdir}Base{ex}{ext}', f'{exdir}Long{ex}{ext}', f'{exdir}Phrase{ex}{ext}', f'{exdir}Term{ex}{ext}']

for l in lexis_ex if ex_b else lexis:
    lexi = load(l)
    full.update(lexi)

base = Lexicon()
if ex_b:
    base.name = 'Base-Extra'
    base.name_zh = '基础词汇扩展'
else:
    base.name = 'Base'
    base.name_zh = '基础词汇'
long = Lexicon()
if ex_b:
    long.name = 'Long-Extra'
    long.name_zh = '长词汇扩展'
else:
    long.name = 'Long'
    long.name_zh = '长词汇'
phrase = Lexicon()
if ex_b:
    phrase.name = 'Phrase-Extra'
    phrase.name_zh = '短语扩展'
else:
    phrase.name = 'Phrase'
    phrase.name_zh = '短语'
term = Lexicon()
if ex_b:
    term.name = 'Term-Extra'
    term.name_zh = '术语扩展'
else:
    term.name = 'Term'
    term.name_zh = '术语'

for word in full:  # [phonetic, definition, translation, exchanges]
    full[word][2] = full[word][2].replace(r'\n', '\n').strip()
    full[word][1] = full[word][1].replace(r'\n', '\n').strip()
    result = full[word]
    term_b = True
    for t in result[2].splitlines():
        if t.strip() and not t.startswith('['):
            term_b = False
    if term_b:
        term[word] = result
    elif ' ' in word:
        phrase[word] = result
    elif len(word) >= 10:
        long[word] = result
    else:
        base[word] = result

if ex_b:
    dump(f'{exdir}Base{ex}{ext}', base)
    dump(f'{exdir}Long{ex}{ext}', long)
    dump(f'{exdir}Phrase{ex}{ext}', phrase)
    dump(f'{exdir}Term{ex}{ext}', term)
else:
    dump(f'{dir}Base{ext}', base)
    dump(f'{dir}Long{ext}', long)
    dump(f'{dir}Phrase{ext}', phrase)
    dump(f'{dir}Term{ext}', term)
