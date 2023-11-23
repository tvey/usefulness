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


def get_result(method: str, params: dict) -> list:
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'id': 123,
        'params': {'apiKey': API_KEY} | params,
    }
    json_data = json.dumps(data)
    r = requests.post(BASIC_API_URL, data=json_data, headers=headers)
    r_data = r.json()
    print(r_data)

    if not r.ok:
        raise Exception(r_data['error']['message'])

    try:
        result = r_data['result']['random']['data']
        return result
    except KeyError:
        pass


def get_random_integers(n: int, min_value: int, max_value: int) -> list[int]:
    method = 'generateIntegers'
    params = {
        'n': n,
        'min': min_value,
        'max': max_value,
        'replacement': False,
    }
    return get_result(method, params)


def get_random_integer_sequences(
    n: int,
    length: int | list[int],
    min_values: int | list[int],
    max_values: int | list[int],
    replacement: bool = False,
) -> list[list[int]]:
    method = 'generateIntegerSequences'
    params = {
        'n': n,
        'length': length,
        'min': min_values,
        'max': max_values,
        'replacement': replacement,
        'base': 10,
    }
    return get_result(method, params)


def get_random_strings(
    n: int, length: int, chars: str, replacement: bool = True
) -> list[str]:
    method = 'generateStrings'
    params = {
        'n': n,
        'length': length,
        'characters': chars,
        'replacement': replacement,
    }
    return get_result(method, params)
