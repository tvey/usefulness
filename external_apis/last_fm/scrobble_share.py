import os
import time

import dotenv
import requests

from last_fm.utils import write_to_file

dotenv.load_dotenv()


def get_artists() -> dict[str, int]:
    api_key = os.getenv("API_KEY")
    username = os.getenv("LASTFM_USER")
    base_url = "https://ws.audioscrobbler.com/2.0/"
    page = 1
    params = {
        "method": "library.getArtists",
        "user": username,
        "api_key": api_key,
        "format": "json",
        "limit": 200,
    }
    artist_scrobbles = {}

    while True:
        params["page"] = page
        response = requests.get(base_url, params=params)
        data = response.json()

        if not data.get("artists", {}).get("artist"):
            break

        artists = data["artists"]["artist"]

        for artist in artists:
            name = artist["name"]
            playcount = int(artist["playcount"])
            artist_scrobbles[name] = playcount

        print(f"Got page {page}")
        page += 1
        time.sleep(0.5)

    return artist_scrobbles


if __name__ == "__main__":
    artist_scrobbles = get_artists()
    sorted_artists = dict(
        sorted(artist_scrobbles.items(), key=lambda x: x[1], reverse=True)
    )
    write_to_file(artist_scrobbles)
