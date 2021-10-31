import os
import json
import random
import string

import pytest
import dotenv

from ..youtube import YouTube

dotenv.load_dotenv()


def load_ids():
    with open('tests/ids.json') as f:
        return json.load(f)


@pytest.fixture
def valid_key():
    return os.environ.get('YOUTUBE_DATA_API_KEY')


@pytest.fixture
def yt(valid_key):
    return YouTube(valid_key)


@pytest.fixture
def long_playlist_id():
    long_playlist_ids = [
        'PLf6Ove6NWsVdHPONgi-c_4I0LOobNDVLt',
        'PLoaTLsTsV3hPJDj7YaE1p0k-Pp1GdWPcV',
    ]
    return random.choice(long_playlist_ids)


@pytest.fixture
def playlist_ids():
    def _playlist_ids(num):
        playlist_ids = load_ids().get('playlists')
        return random.sample(playlist_ids, k=num)

    return _playlist_ids


@pytest.fixture
def video_ids():
    def _video_ids(num):
        video_ids = load_ids().get('videos')
        return random.sample(video_ids, k=num)

    return _video_ids


@pytest.fixture
def video_id():
    video_ids = load_ids().get('videos')
    return random.choice(video_ids)


@pytest.fixture
def channel_id():
    channel_ids = load_ids().get('channels')
    return random.choice(channel_ids)


@pytest.fixture
def random_string():
    letters = string.ascii_letters
    random_chars = random.choices(string.printable, k=random.randint(1, 30))
    random_letters = random.choices(letters, k=random.randint(1, 30))
    return ''.join(random.choice([random_chars, random_letters]))
