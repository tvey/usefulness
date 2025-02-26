import os
import time

import dotenv
import requests

dotenv.load_dotenv()


def get_artists() -> dict:
    api_key = os.getenv('API_KEY')
    username = os.getenv('LASTFM_USER')
    base_url = 'https://ws.audioscrobbler.com/2.0/'
    page = 1
    params = {
        'method': 'library.getArtists',
        'user': username,
        'api_key': api_key,
        'format': 'json',
        'limit': 200,
    }
    artist_scrobbles = {}

    while True:
        params['page'] = page
        response = requests.get(base_url, params=params)
        data = response.json()

        if not data.get("artists", {}).get("artist"):
            break

        artists = data['artists']['artist']

        for artist in artists:
            name = artist['name']
            playcount = int(artist['playcount'])
            artist_scrobbles[name] = playcount

        page += 1
        time.sleep(0.5)

    return artist_scrobbles


artist_scrobbles = get_artists()
total_scrobbles = sum(artist_scrobbles.values())
artist_share = {
    artist: (count / total_scrobbles) * 100 for artist, count in artist_scrobbles.items()
}
sorted_artists = sorted(artist_share.items(), key=lambda x: x[1], reverse=True)

print(f'Total scrobbles: {total_scrobbles}')

for artist, share in sorted_artists:
    print(f'{artist}: {artist_scrobbles.get(artist)} scrobbles ({share:.2f}%)')
