from urllib.parse import urlparse
from http import client
from json import loads

def get(url, timeout=3):
    parsed_url = urlparse(url)
    conn = client.HTTPSConnection(parsed_url.netloc, timeout=timeout)
    conn.request("GET", parsed_url.path + "?" + parsed_url.query)
    res = conn.getresponse()
    if res.status != 200:
        raise Exception(f"HTTP request failed with status {res.status}")
    data = res.read()
    conn.close()
    try: return loads(data)
    except: return data
