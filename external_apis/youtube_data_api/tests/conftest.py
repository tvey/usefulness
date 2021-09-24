import os
import random
import string

import pytest
import dotenv

from ..youtube import YouTube

dotenv.load_dotenv()


@pytest.fixture
def valid_key():
    return os.environ.get('YOUTUBE_DATA_API_KEY')


@pytest.fixture
def yt(valid_key):
    return YouTube(valid_key)


@pytest.fixture
def long_playlist_id():
    return YouTube(valid_key)


@pytest.fixture
def playlist_id():
    return YouTube(valid_key)


@pytest.fixture
def video_id():
    pass


@pytest.fixture
def video_list():
    pass
 

@pytest.fixture
def random_string():
    chars = list(string.printable)
    random_chars = random.choices(string.printable, k=random.randint(1, 50))
    random_letters = random.choices(chars, k=random.randint(1, 50))
    return ''.join(random_chars)

