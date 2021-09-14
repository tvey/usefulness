import json

import requests

# import requests_cache


class YouTube:
    """Example of YouTube Data API wrapper with a limited functionality."""

    def __init__(self, api_key, region='US'):
        self.base_url = 'https://www.googleapis.com/youtube/v3/'
        self.region = region
        self.api_key = api_key
        self.params = {
            'key': self.api_key,
            'part': 'snippet',
            'maxResults': 50,
            'nextPageToken': '',
        }

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        url = f'{self.base_url}videos?id=nGeKSiCQkPw&fields=items/kind'
        r = requests.get(url, params={'key': value, 'part': 'snippet'})

        if r.status_code == 400 or r.status_code == 403:
            raise ValueError('Please use a valid API key.')
        else:
            self._api_key = value

    def search(self, query):
        resource = 'search'
        url = f'{self.base_url}{resource}'
        search_params = self.params | {'q': query, 'regionCode': self.region}
        return self._get_response(url, search_params)

    def videos(self, video_ids):
        resource = 'videos'

    def playlists(self, playlist_id):
        resource = 'playlists'

    def playlist_items(self):
        resource = 'playlistItems'

    def _get_response(self, url, params):
        """Send a request and return a valid response or an error message."""
        # session = requests_cache.CachedSession('youtube_cache')
        # r = session.get(url, params=params)
        r = requests.get(url, params)

        if r.status_code != 200:
            try:
                r.json()
            except json.decoder.JSONDecodeError:
                raise Exception('Cannot call the API.')

            error_message = r.json().get('error').get('message')
            return {'code': r.status_code, 'message': error_message}

        # if page_token in params - recurse?
        return r.json()

    def __write(self, data, filename):
        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
