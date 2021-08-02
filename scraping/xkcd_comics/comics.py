"""Probably you want to have all the xkcd comics locally.
Sync version for now, so it's going to take some time.
"""

import os
import re
import time
import random

import requests
from requests_html import HTMLSession


BASE_URL = 'https://xkcd.com/'


def get_latest() -> int:
    """Return id of the latest comic on the site."""
    r = requests.get(BASE_URL)
    comic_regex = re.compile(
        r"Permanent link to this comic: https:\/\/xkcd.com\/(\d+)\/<br \/>"
    )
    match = comic_regex.search(r.text)
    return int(match.group(1))


def get_comic(session, num) -> dict:
    """Get comic page and extract desired data."""
    html = session.get(f'{BASE_URL}{num}').html

    title = html.find('#ctitle', first=True).text
    image_elem = html.find('#comic img', first=True)
    image_src = html._make_absolute(image_elem.attrs['src'])  # hackish, yep
    filename = image_src.rsplit('/', maxsplit=1)[-1]

    if image_elem.attrs.get('srcset'):
        src = image_elem.attrs['srcset'].strip(' 2x')
        image_src = html._make_absolute(src)
    ext = os.path.splitext(image_src)[-1]
    title_filename = title.replace(' ', '_').replace('/', '_')
    filename = f"{num:>04d}_{title_filename}{ext}"

    return {
        'id': num,
        'title': title,
        'filename': filename,
        'image_src': image_src,
    }


def write_comic(num, folder) -> None:
    """Request image url and write response content to a file."""
    session = HTMLSession()
    os.makedirs(folder, exist_ok=True)
    comic = get_comic(session, num)
    print(f'{num}: {comic["title"]}')
    r = session.get(comic['image_src'])

    if r.status_code == 200:
        with open(f"{folder}/{comic['filename']}", 'wb') as image_file:
            for chunk in r.iter_content(100000):
                image_file.write(chunk)


def get_comics(folder='comics', sleep=True) -> None:
    """Write all comics."""
    latest = get_latest()
    start = time.perf_counter()
    print("Starting, it's time for tea 🍵\nOr maybe for the whole meal... 🙃")
    print(f'Latest comic: {latest}')

    for i in range(1, latest + 1):
        # not typical comics, sorry
        if i in [404, 961, 1037, 1116, 1264, 1350, 1416, 1608, 1663, 2198]:
            continue
        write_comic(i, folder)
        if sleep:
            time.sleep(random.random() * 3)
        if not i % 50:
            mid = time.perf_counter() - start
            pct_done = i * 100 / latest
            print(f'{pct_done:.0f}% done, {mid / 60:.0f} minutes passed')

    end = time.perf_counter()
    print(f'Done in {(end - start) / 60:.0f} minutes')


if __name__ == '__main__':
    get_comics()
