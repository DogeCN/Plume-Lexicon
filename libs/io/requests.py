from libs.io.stdout import print
from urllib.parse import urlparse
from http import client
from json import loads


def get(url, timeout=3):
    try:
        url = urlparse(url)
        conn = client.HTTPSConnection(url.netloc, timeout=timeout)
        conn.request(
            "GET", url.path + "?" + url.query, headers={"User-Agent": "Mozilla/5.0"}
        )
        res = conn.getresponse()
        if res.status != 200:
            return
        data = res.read()
        conn.close()
    except Exception as e:
        print(e, "Red")
        return
    try:
        return loads(data)
    except:
        return data
