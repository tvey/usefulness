import random

import pytest

from ..youtube import APIException, YouTube


def test_instance_init_with_valid_key(valid_key):
    assert YouTube(valid_key)


def test_instance_init_with_invalid_key():
    with pytest.raises(ValueError):
        assert YouTube('abc123')


def test_existing_attributes(yt):
    assert hasattr(yt, 'api_key')
    assert hasattr(yt, 'params')
    assert hasattr(yt, '_get_response')
    assert hasattr(yt, 'search')
    assert hasattr(yt, 'videos')
    assert hasattr(yt, 'playlists')
    assert hasattr(yt, 'playlist_items')
    assert not hasattr(yt, 'channels')


def test_request_response_items_list(yt, playlist_ids, video_ids, channel_id):
    random_num = random.randint(1, 20)
    video_result = yt.videos(video_ids(random_num))
    playlist_result = yt.playlists(playlist_ids(random_num))
    channel_result = yt.playlists(channel_id=channel_id)

    assert len(playlist_result) == random_num
    assert len(video_result) == random_num
    assert channel_result


@pytest.mark.skip
def test_get_response_looping(yt, long_playlist_id):
    result = yt.playlist_items(long_playlist_id)

    assert len(result) > 50
    assert len(result) > 900  # i know it


def test_search_returns_expected_result(yt):
    result = yt.search('doge')

    assert result
    assert len(result) == 50  # search defaults to 50 results max in the class
    assert random.choice(result).get('kind') == 'youtube#searchResult'


def test_search_returns_empty_result(yt):
    result = yt.search('mwqwourfyv')

    assert result == []


def test_videos_multiple_ids(yt, video_ids):
    ids = video_ids(random.randint(2, 10))
    result = yt.videos(ids)

    assert len(result) == len(ids)
    assert result[0].get('kind') == 'youtube#video'


def test_videos_returned_fields(yt, video_id):
    result = yt.videos(video_id)
    item = result[0]

    assert len(result) == 1  # as one id passed
    assert item.get('kind') == 'youtube#video'
    assert item.get('snippet')
    assert item.get('statistics')


def test_playlists_without_params_raises(yt):
    with pytest.raises(ValueError) as e:
        yt.playlists()

    assert 'either playlist_ids or channel_id' in e.value.args[0]


def test_playlists_incompatible_params_cause_error(
    yt, playlist_ids, channel_id
):
    with pytest.raises(APIException):
        yt.playlists(playlist_ids(2), channel_id=channel_id)


def test_playlists_with_playlists_param(yt, playlist_ids):
    pl_id = playlist_ids(1)[0]
    pl_ids = playlist_ids(random.randint(2, 10))
    result1 = yt.playlists(pl_id)
    result2 = yt.playlists(pl_ids)

    assert result1
    assert result2
    assert len(result1) == 1
    assert len(result2) > 1
    assert result1[0]['kind'] == 'youtube#playlist'


def test_playlists_with_channel_param(yt, channel_id):
    result = yt.playlists(channel_id=channel_id)
    assert result
    assert result[0]['kind'] == 'youtube#playlist'


def test_playlist_items_with_valid_playlist_id(yt, playlist_ids):
    playlist_id = playlist_ids(1)[0]
    result = yt.playlist_items(playlist_id)
    assert result
    assert result[0]['kind'] == 'youtube#playlistItem'


def test_playlist_items_with_invalid_playlist_id_raises(yt):
    with pytest.raises(APIException):
        yt.playlist_items('abc123')
