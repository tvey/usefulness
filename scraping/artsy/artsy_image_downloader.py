import os
import re
import urllib.parse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ARTIST_URL = ''  # https://www.artsy.net/artist/...
ARTWORK_URL = ''  # https://www.artsy.net/artwork/...


def get_artwork_urls(artist_url: str) -> list:
    """Get a list of artwork urls from the artist's page."""
    r = requests.get(artist_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    elems = soup.find_all('a', attrs={'class': ['GridItem__Link-d2n1vy-0']})
    urls = [urljoin('https://www.artsy.net/', a['href']) for a in elems]
    return list(set(urls))


def save_image(artwork_url: str, save_to: str = '.') -> None:
    r = requests.get(artwork_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1').find('i').text
    image = soup.find('img', attrs={'data-testid': 'artwork-lightbox-image'})
    image_src = image['src']
    img_url_encoded = re.search(r'src=(https.+jpg)', image_src).group(1)
    image_url = urllib.parse.unquote(img_url_encoded)
    ext = image_url.rsplit('.')[-1]
    title = f'{title}.{ext}'
    image_path = os.path.join(save_to, title)

    r = requests.get(image_url)

    with open(image_path, 'wb') as f:
        f.write(r.content)
    print('✓', image_path)


if __name__ == '__main__':
    if ARTWORK_URL:
        save_image(ARTWORK_URL)
    elif ARTIST_URL:
        urls = get_artwork_urls(ARTIST_URL)

        if urls:
            print(f'{len(urls)} artworks found, downloading')
            for url in urls:
                save_image(url)
        else:
            print('No artworks for this artist')
