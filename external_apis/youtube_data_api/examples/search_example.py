import os
import html
import json

import dotenv
import requests

dotenv.load_dotenv()


def search(query='piano cat'):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'q': query,
        'key': os.environ.get('YOUTUBE_DATA_API_KEY'),
        'part': ['snippet'],
        'maxResults': 50,
        'order': 'relevance',
        'regionCode': 'GB',
    }

    r = requests.get(url, params=params)
    result = r.json()

    if r.status_code == 200:
        forbidden = '\\/:*?"<>|%.,;= '
        trans_table = str.maketrans(forbidden, '_' * len(forbidden))
        filename = query.translate(trans_table).strip(' _').replace('__', '_')
        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        for item in result['items']:
            title = item['snippet']['title']
            print(html.unescape(title))
    else:
        print(r.status_code, result['error']['message'])


if __name__ == '__main__':
    search()
