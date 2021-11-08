"""Get metadata for the the Huberman Lab Podcast from YouTube Data API."""

import json
import os

import humanize
import isodate
import requests
from dateutil import parser
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = os.environ.get('YOUTUBE_DATA_API_KEY')


def format_duration(seconds: int) -> str:
    humanized = humanize.precisedelta(
        seconds,
        format='%0.0f',
        suppress=['days'],
    )
    return humanized.replace(' and', ',')


def format_date(s: str) -> str:
    dt = parser.parse(s)
    return dt.strftime('%Y-%m-%d')


def get_items_meta(item_ids: list) -> list:
    params = {
        'key': API_KEY,
        'part': ['contentDetails', 'snippet', 'statistics'],
        'id': ','.join(item_ids),
    }
    r = requests.get(f'{BASE_URL}videos', params=params)
    items = r.json().get('items')
    result = []

    if items:
        for item in items:
            video = {}
            duration = isodate.parse_duration(
                item['contentDetails']['duration']
            ).total_seconds()
            video['#'] = int(item['snippet']['title'].rsplit('#', 1)[-1])
            video['video_id'] = item['id']
            video['title'] = item['snippet']['title']
            video['date'] = format_date(item['snippet']['publishedAt'])
            # video['description'] = item['snippet']['description']
            video['views'] = int(item['statistics']['viewCount'])
            video['likes'] = int(item['statistics']['likeCount'])
            video['dislikes'] = int(item['statistics']['dislikeCount'])
            video['comments'] = int(item['statistics']['commentCount'])
            video['duration_seconds'] = int(duration)
            video['duration_str'] = format_duration(int(duration))
            result.append(video)

    return result


def get_playlist_meta(playlist_id: str) -> dict:
    params = {
        'key': API_KEY,
        'part': ['snippet', 'contentDetails'],
        'id': playlist_id,
    }
    r = requests.get(f'{BASE_URL}playlists', params=params)

    if r.json().get('items'):
        data = r.json().get('items')[0]
        return {
            'channel_title': data['snippet']['channelTitle'],
            'playlist_title': data['snippet']['title'],
            'item_count': data['contentDetails']['itemCount'],
            'published_at': format_date(data['snippet']['publishedAt']),
            'playlist_description': data['snippet']['description'],
        }
    return {}


def get_result(playlist_id: str) -> dict:
    """Playlist meta + items meta."""
    url = f'{BASE_URL}playlistItems'
    params = {
        'key': API_KEY,
        'part': ['snippet'],
        'playlistId': playlist_id,
        'maxResults': 50,
        'pageToken': '',
    }
    videos_meta = []

    while True:
        r = requests.get(url, params=params)
        data = r.json()

        if not data.get('items'):
            if data.get('error'):
                return {
                    'error': data.get('error').get('message'),
                    'code': data.get('error').get('code'),
                }
            else:
                return {}

        item_ids = [
            v['snippet']['resourceId']['videoId'] for v in data['items']
        ]
        videos_meta += get_items_meta(item_ids)

        next_page_token = data.get('nextPageToken')

        if not next_page_token:
            break
        params['pageToken'] = next_page_token

    playlist_meta = get_playlist_meta(playlist_id)
    total_duration = sum([v['duration_seconds'] for v in videos_meta])
    playlist_meta['duration_seconds'] = total_duration
    playlist_meta['duration_str'] = format_duration(total_duration)
    videos_meta.sort(key=lambda v: v['#'])

    return {
        'playlist': playlist_meta,
        'items': videos_meta,
    }


if __name__ == '__main__':
    huberman_lab_podcast = 'PLPNW_gerXa4Pc8S2qoUQc5e8Ir97RLuVW'

    with open('huberman_lab.json', 'w', encoding='utf-8') as f:
        data = get_result(huberman_lab_podcast)
        json.dump(data, f, ensure_ascii=False, indent=4)
