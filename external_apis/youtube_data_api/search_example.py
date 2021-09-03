import os
import html
import json

import requests
from dotenv import load_dotenv

load_dotenv()

base_url = 'https://www.googleapis.com/youtube/v3/'
query = 'piano cat'

params = {
    'q': query,
    'key': os.environ.get('YOUTUBE_DATA_API_KEY'),
    'part': ['snippet'],
    'maxResults': 50,
    'order': 'relevance',
    'regionCode': 'GB',
}


def search(query=query):
    search_url = f'{base_url}search'
    print(params)
    r = requests.get(search_url, params=params)
    result = r.json()

    if r.status_code == 200:
        filename = query.replace(' ', '_')
        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        for item in result['items']:
            title = item['snippet']['title']
            print(html.unescape(title))
    else:
        print(r.status_code, result['error']['message'])


if __name__ == '__main__':
    search()
