import pytest

from ..youtube import YouTube


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


@pytest.mark.calling
def test_search(valid_key):
    yt = YouTube(valid_key)
    result = yt.search('doge')

    assert result['kind'] == 'youtube#searchListResponse'
    assert result['items']
