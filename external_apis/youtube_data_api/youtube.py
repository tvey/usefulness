import re
import json
import copy

import requests
import requests_cache

requests_cache.install_cache('youtube_cache')


class APIException(Exception):
    pass


class YouTube:
    """YouTube Data API wrapper that gets selected resources.

    Utilizes only list (GET) method for each endpoint.
    Screams (raises) when there's an error (from YouTube API or other).

    Attributes:
        api_key: A valid key for enabled YouTube Data API v3.
        region: ISO 3166-1 country code.
    """

    def __init__(self, api_key, region='US'):
        self.base_url = 'https://www.googleapis.com/youtube/v3/'
        self.region = region
        self.api_key = api_key
        self.params = {
            'key': self.api_key,
            'part': ['snippet'],
            'maxResults': 50,
            'pageToken': '',
        }

    @property
    def api_key(self):
        """https://developers.google.com/youtube/v3/getting-started"""
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        url = f'{self.base_url}videos?id=nGeKSiCQkPw&fields=items/kind'
        r = requests.get(url, params={'key': value, 'part': 'snippet'})

        if r.status_code == 400 or r.status_code == 403:
            raise ValueError('Please use a valid API key.')
        elif r.status_code != 200:
            raise APIException('Cannot initiate YouTube.')
        else:
            self._api_key = value

    def search(self, query):
        """Get info about resources matching a query from the search endpoint.

        Match videos, channels, and playlists, ordered by relevance.
        Retrieve first 50 search results.
        Quota cost — 100 units.
        """
        resource = 'search'
        search_params = copy.deepcopy(self.params) | {
            'q': query,
            'regionCode': self.region,
        }
        return self._get_response(resource, search_params, loop=False)

    def videos(self, video_ids):
        """Retrieve data about one or more videos.

        Quota cost — 1 unit.
        """
        resource = 'videos'
        params = copy.deepcopy(self.params) | {'id': video_ids}
        params['part'].append('statistics')
        return self._get_response(resource, params)

    def playlists(self, playlist_ids=None, channel_id=None):
        """Retrieve data about playlists.

        Parameters (two mutually exclusive ways of using the endpoint):
            playlist_ids: one id (or multiple ids as a list)
            channel_id: accessing channel's playlists (one channel only)

        If none or both parameters are passed, APIException is raised.

        Quota cost — 1 unit.
        """
        resource = 'playlists'

        if playlist_ids and channel_id:
            msg = 'Incompatible parameters. Use playlist_ids *or* channel_id.'
            raise APIException(msg)
        elif not playlist_ids and not channel_id:
            raise ValueError('Pass either playlist_ids or channel_id.')

        params = copy.deepcopy(self.params)
        params['part'].append('contentDetails')

        if playlist_ids:
            params = params | {'id': playlist_ids}
        elif channel_id:
            params = params | {'channelId': channel_id}

        return self._get_response(resource, params)

    def playlist_items(self, playlist_id):
        """Get items of a passed playlist.

        Accept a valid playlist id.
        Quota cost — 1 unit.
        """
        resource = 'playlistItems'
        params = copy.deepcopy(self.params) | {'playlistId': playlist_id}
        return self._get_response(resource, params)

    def _get_response(self, resource, params, loop=True) -> list:
        """Send a request and return a valid response or an empty list.

        Extract and return 'items' of the API responses.
        Raise with a returned message in case of any API response errors.

        Accept a resource name and its relevant prepared params.
        Params are accepted as a dict and encoded by Requests.
        If loop is set to True, access all pages in a paged response.
        """
        url = f'{self.base_url}{resource}'
        r = requests.get(url, params)

        if r.status_code != 200:
            try:
                r.json()
            except json.decoder.JSONDecodeError:
                raise APIException('Cannot call the API.')
            raise APIException(r.json().get('error').get('message'))

        result = r.json().get('items', [])
        next_page_token = r.json().get('nextPageToken')

        if not loop or not next_page_token:
            return result
        elif next_page_token:
            while True:
                params['pageToken'] = next_page_token
                r = requests.get(url, params=params)
                items = r.json().get('items', [])
                result.extend(items)

                next_page_token = r.json().get('nextPageToken')
                if not next_page_token:
                    break

        return result

    def _write(self, data, filename):
        """Dump result to a file.

        Accept a valid json data and a filename without extension.
        """
        forbidden_chars = '\\/:*?"<>|%.,;='
        t_table = str.maketrans(forbidden_chars, '_' * len(forbidden_chars))
        filename = filename.translate(t_table).strip('_').replace('__', '_')

        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
