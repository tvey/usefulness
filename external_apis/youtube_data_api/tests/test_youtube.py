import random

import pytest

from ..youtube import YouTube, APIException


def test_instance_init_with_valid_key(valid_key):
    assert YouTube(valid_key)


def test_instance_init_with_invalid_key():
    with pytest.raises(ValueError):
        assert YouTube('12345')


def test_existing_attributes(yt):
    assert hasattr(yt, 'api_key')
    assert hasattr(yt, 'params')
    assert hasattr(yt, '_get_response')
    assert hasattr(yt, 'search')
    assert hasattr(yt, 'videos')
    assert hasattr(yt, 'playlists')
    assert hasattr(yt, 'playlist_items')
    assert not hasattr(yt, 'channels')


@pytest.mark.calling
def test_request_reponse_items(yt):
    pass


@pytest.mark.calling
def test_search_returns_expected_result(yt):
    result = yt.search('doge')

    assert result
    assert len(result) == 50  # max page size, default in the class
    assert random.choice(result).get('kind') == 'youtube#searchResult'


@pytest.mark.calling
def test_search_returns_no_result(yt):
    result = yt.search('mwqwourfyv')

    assert result == []

