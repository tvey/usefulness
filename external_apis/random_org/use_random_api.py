import json
import os

import dotenv
import requests

dotenv.load_dotenv()

BASIC_API_URL = 'https://api.random.org/json-rpc/2/invoke'
API_KEY = os.getenv('API_KEY')

headers = {
    'content-type': 'application/json',
}


def get_random_integers(n: int, min_value: int, max_value: int) -> list[int]:
    data = {
        'jsonrpc': '2.0',
        'method': 'generateIntegers',
        'id': 123,
        'params': {
            'apiKey': API_KEY,
            'n': n,
            'min': min_value,
            'max': max_value,
            'replacement': False,
        },
    }
    json_data = json.dumps(data)

    r = requests.post(BASIC_API_URL, data=json_data, headers=headers)
    r_data = r.json()

    if not r.ok:
        raise Exception(r_data['error']['message'])

    try:
        ints = r_data['result']['random']['data']
        return ints
    except KeyError:
        pass
