from libs.io.stdout import print
from urllib.parse import urlparse
from http import client
from json import loads


def get(url, timeout=3):
    try:
        parsed_url = urlparse(url)
        conn = client.HTTPSConnection(parsed_url.netloc, timeout=timeout)
        conn.request("GET", parsed_url.path + "?" + parsed_url.query)
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
