import os
import json
import time
import argparse

import requests


class APIException(Exception):
    pass


class FoodData:
    """Wrapper for a FoodData Central API."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nal.usda.gov/fdc/v1'
        self.data_type = 'Foundation,Survey (FNDDS),SR Legacy'
        self.page_size = 100

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        url = f'https://api.nal.usda.gov/fdc/v1/json-spec?api_key={value}'
        r = requests.get(url)

        if r.status_code == 400 or r.status_code == 403:
            raise APIException(r.json()['error']['message'])
        else:
            self._api_key = value

    def _write_data(self, data, filename) -> None:
        """Write data to a json file. Filename param - without extension."""
        os.makedirs('data', exist_ok=True)
        filename = filename.replace(' ', '_')

        with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'File “{filename}.json” is created in data/ folder.')

    def search(self, query, nutrients=True, write=False) -> list:
        """Return formatted results of a search response based on a query."""
        if not str(query).strip():
            raise ValueError('Query cannot be empty.')

        params = {
            'api_key': self.api_key,
            'pageSize': self.page_size,
            'dataType': self.data_type,
            'query': query,
        }

        r = requests.get(f'{self.base_url}/search', params=params)

        if r.status_code != 200:
            print(r.json())
            raise APIException(r.json()['error'])

        foods = r.json().get('foods')
        if not foods:
            return []

        result = []
        print(f'Getting results for “{query}”...')
        time.sleep(1)

        for food in foods:
            elem = {
                'id': food['fdcId'],
                'name': food['description'],
                'category': food['foodCategory'],
            }
            if nutrients:
                food_nutrients = {}

                for n in food['foodNutrients']:
                    n_name = n['nutrientName']
                    n_value = f"{n['value']} {n['unitName'].lower()}"
                    food_nutrients[n_name] = n_value
                elem['nutrients'] = food_nutrients

            result.append(elem)

        if write:
            self._write_data(result, query)

        return result

    def get_ids(self, query, write=False) -> list:
        """Search but return a list of tuples (food_id, food_name)"""

        foods = self.search(query, nutrients=False)

        if not foods:
            return []

        result = [(food['id'], food['name']) for food in foods]

        if write:
            result_to_write = [{'id': i[0], 'name': i[1]} for i in result]
            self._write_data(result_to_write, f'{query}_ids')

        return result

    def get_foods(self, food_ids, write=False) -> list:
        """Fetch from FDC data for a particular foods based on their ids."""
        if isinstance(food_ids, int):
            ids = str(food_ids)
        elif isinstance(food_ids, (list, tuple, str)):
            if not all([str(i).isdigit() for i in food_ids]):
                raise TypeError('Food ids must be numbers.')
            ids = ','.join([str(i) for i in list(food_ids)])
        else:
            raise TypeError('Pass food ids as numbers or a list of numbers.')

        url = f'{self.base_url}/foods/?fdcIds={ids}&api_key={self.api_key}'
        r = requests.get(url)

        if r.status_code != 200:
            raise APIException(r.json().get('message'))

        food_data = r.json()

        result = []

        for item in food_data:
            item_data = {'id': item['fdcId'], 'name': item['description']}

            nutrients = {}

            if item.get('foodNutrients'):
                for n in item['foodNutrients']:
                    if n.get('amount'):
                        n_name = n['nutrient']['name']
                        n_unit = n['nutrient']['unitName'].lower()
                        n_amount = n['amount']
                        n_value = f'{n_amount:.2f} {n_unit}'
                        nutrients[n_name] = n_value
                item_data['nutrients'] = nutrients
            result.append(item_data)

        if write:
            self._write_data(result, ids)

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='fooddata',
        usage='%(prog)s api_key query --get_ids --write',
        description=('Get food data from FoodData Cental API.'),
    )
    parser.add_argument(
        'api_key',
        help='Valid API key, get it signing up on https://fdc.nal.usda.gov/',
    )
    parser.add_argument('query', help='Either a search string or a food id.')
    parser.add_argument(
        '-ids',
        '--get-ids',
        help='Search and get abridged results in a form of food ids and names.',
        nargs='?',
        const=True,
        default=False,
    )
    parser.add_argument(
        '-w',
        '--write',
        help='Write results to a file locally.',
        nargs='?',
        const=True,
        default=True,
    )
    args = parser.parse_args()

    fd = FoodData(args.api_key)

    if fd:
        query = args.query
        write = args.write

        if not query.isdigit():
            fd.search(query, write=write)
        elif args.get_ids:
            fd.get_ids(query, write=write)
        else:
            fd.get_foods(query, write=write)
    else:
        print('Cannot initiate FoodData.')
