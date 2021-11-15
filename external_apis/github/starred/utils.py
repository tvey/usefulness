import json
import os

import dotenv

dotenv.load_dotenv()

gh_token = os.environ.get('PERSONAL_ACCESS_TOKEN')

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {gh_token}',
}

base_url = 'https://api.github.com'

starred_url = f'{base_url}/user/starred'  # no trailing slash


def dump_to_print(data):
    print(json.dumps(data, indent=4))


def dump_to_file(data, filename_base):
    with open(f'{filename_base}.json', 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=4, ensure_ascii=False)


def check_data(file):
    with open(file) as fh:
        data = json.load(fh)
        print(len(data))
