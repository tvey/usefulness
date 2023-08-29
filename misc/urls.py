import urllib.parse


def decode(url: str) -> str:
    return urllib.parse.unquote(url)


def encode(url: str) -> str:
    return urllib.parse.quote(url)


url = 'https://zh.wikipedia.org/wiki/%E7%8C%AB%E7%A7%91'
decoded_url = decode(url)
assert '猫' in decoded_url

url_2 = 'https://ru.wikipedia.org/wiki/Лесной_кот'
encoded_url = encode(url_2)
assert 'кот' not in encoded_url
