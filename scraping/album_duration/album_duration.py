from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ARTIST_URL = ''  # https://<artist>.bandcamp.com/music
ALBUM_URL = ''  # https://<artist>.bandcamp.com/album/<album>


def get_albums_info(artist_url: str) -> list[dict]:
    albums_info = []
    r = requests.get(artist_url)
    if r.status_code == 404:
        raise ValueError("Check your artist_url value, page not found")
    soup = BeautifulSoup(r.text, 'html.parser')
    album_list_elem = soup.find('ol', id='music-grid')
    album_links = album_list_elem.select('a[href*=album]')

    for link in album_links:
        album = {}
        base_url = artist_url.removesuffix('music')
        album['url'] = urljoin(base_url, link['href'])
        album['title'] = link.select_one('p.title').text.strip()
        albums_info.append(album)
    return albums_info


def get_total_duration(durations: list[str]) -> int:
    durations_dt = [datetime.strptime(i, '%M:%S') for i in durations]
    deltas = [
        timedelta(minutes=i.minute, seconds=i.second) for i in durations_dt
    ]
    return int(sum(deltas, timedelta()).total_seconds())


def pluralize(amount: int, unit: str) -> str:
    amount = int(amount)
    if amount == 0:
        return ''
    elif amount > 1:
        unit += 's'
    return f'{amount} {unit}'


def format_seconds(seconds: int, is_single: bool = False) -> str:
    h, s = divmod(seconds, 3600)
    m, s = divmod(s, 60)

    if is_single:
        return f"{pluralize(m, 'minute')} {pluralize(s, 'second')}"
    elif h:
        return f"{pluralize(h, 'hour')} {pluralize(m, 'minute')}"
    return f'{m} minutes'


def get_duration_bandcamp(album_url: str, human: bool = True) -> str | int:
    r = requests.get(album_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    track_list = soup.find('table', class_='track_list')
    time_spans = track_list.find_all('span', class_='time')
    durations = [i.text.strip() for i in time_spans]
    n_tracks = len(durations)
    is_single = False
    if n_tracks == 1:
        is_single = True
    total_duration = get_total_duration(durations)

    if human:
        return format_seconds(total_duration, is_single=is_single)
    return total_duration


if __name__ == '__main__':
    if ALBUM_URL:
        album_duration = get_duration_bandcamp(ALBUM_URL)
        print(album_duration)
    elif ARTIST_URL:
        albums = get_albums_info(ARTIST_URL)

        for album in albums:
            album_duration = get_duration_bandcamp(album['url'], human=True)
            print(f"{album['title']}: {album_duration}")
