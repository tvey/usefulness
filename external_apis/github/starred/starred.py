"""Fetching info about useful repos."""
import requests
import requests_cache

from utils import (
    headers,
    starred_url,
    dump_to_file as dtf,
)

requests_cache.install_cache('../github_cache')

r = requests.head(starred_url, headers=headers)
last_page = r.links['last']['url'].rsplit('=')[-1]  # "Links" header

starred = []

for page in range(1, int(last_page) + 1):
    r = requests.get(starred_url, headers=headers, params={'page': page})
    data = r.json()
    if r.ok and data:
        starred += data
        links = r.links

selected_attrs = ['full_name', 'url', 'language', 'topics']
result = [{k: item[k] for k in selected_attrs} for item in starred]

print(f'{len(result)} starred repos')

dtf(result, 'starred')
