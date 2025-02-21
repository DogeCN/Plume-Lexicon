from libs.io.requests import get
from urllib.parse import quote
import info


def apiTranslate(text: str, tl: int = 0 | 1):
    url = info.url_trans % (["zh", "en"][tl], quote(text))
    res = get(url)
    return res[0][0][0]
