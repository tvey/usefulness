import re
import urllib.parse

import requests
from bs4 import BeautifulSoup

URL = ''


def get_image_info(artwork_url: str) -> dict:
    r = requests.get(artwork_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1').find('i').text
    image = soup.find('img', attrs={'data-testid': 'artwork-lightbox-image'})
    image_src = image['src']
    img_url_encoded = re.search(r'src=(https.+jpg)', image_src).group(1)
    image_url = urllib.parse.unquote(img_url_encoded)
    ext = image_url.rsplit('.')[-1]

    return {
        'title': f'{title}.{ext}',
        'url': image_url,
    }


def save_image(image_info: dict) -> None:
    r = requests.get(image_info['url'])

    with open(image_info['title'], 'wb') as f:
        f.write(r.content)


def main():
    image_info = get_image_info(URL)
    save_image(image_info)
