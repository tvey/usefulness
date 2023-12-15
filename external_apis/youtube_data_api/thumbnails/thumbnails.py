import os
import re

import dotenv
import requests

dotenv.load_dotenv()

BASE_URL = 'https://www.googleapis.com/youtube/v3/videos'
API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
VIDEO_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


def get_thumbnails(api_key: str, video_url: str) -> dict:
    video_pattern = r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)'
    match = re.search(video_pattern, video_url)
    if match:
        video_id = match.group()
    else:
        raise ValueError(f'Unable to find the video id: {video_url}')

    params = {
        'id': video_id,
        'key': api_key,
        'part': 'snippet',
    }

    try:
        r = requests.get(BASE_URL, params=params)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    video_info = r.json()
    return video_info['items'][0]['snippet']['thumbnails']  # hm


def download_thumbnail(
    thumbnails_info: dict, quality: str, location: str = '.'
):
    qualities = ['default', 'medium', 'high', 'standard', 'maxres']
    if quality not in qualities:
        raise ValueError(f'Not such quality value: {quality}')

    url = thumbnails_info[quality]['url']  #
    parts = url.split('/')
    filename = f'{parts[-2]}_{parts[-1]}'
    file_path = os.path.join(location, filename)

    try:
        r = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(r.content)
            print(f'Thumbnail_saved: {file_path}')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


thumbnails_info = get_thumbnails(API_KEY, VIDEO_URL)
download_thumbnail(thumbnails_info, 'maxres')
