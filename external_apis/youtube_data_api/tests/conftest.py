import os

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
