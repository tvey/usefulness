import time
import json
import random
import asyncio
from urllib.parse import urljoin

from requests_html import AsyncHTMLSession

BASE_URL = 'https://calorizator.ru/product/all'
NUM_PAGES = 82
URLS = [f'{BASE_URL}?page={i}' for i in range(NUM_PAGES + 1)]


async def get_response(asession, url):
    """Get url with async session and return the HTMLResponse."""
    r = await asession.get(url)

    sleep_time = random.random() * 2
    await asyncio.sleep(sleep_time)
    return r


async def await_responses(urls):
    """Gather tasks for event loop."""
    asession = AsyncHTMLSession()
    tasks = (get_response(asession, url) for url in urls)
    return await asyncio.gather(*tasks)


def get_page_products(r):
    """Collect items from a given page and return them as a list of dicts."""
    print(r.url)
    page_products = []
    table = r.html.find('.views-table', first=True)
    rows = table.find('tbody tr.odd') + table.find('tbody tr.even')

    for row in rows:
        product = {}
        tds = row.find('td')
        product['name'] = tds[1].find('a', first=True).text
        href = tds[1].find('a', first=True).attrs.get('href')
        product['url'] = urljoin(BASE_URL, href)
        product['category'] = product['url'].rsplit('/', maxsplit=2)[-2]
        try:
            product['cals'] = float(tds[-1].text.strip())
            product['prot'] = float(tds[2].text.strip())
            product['fat'] = float(tds[3].text.strip())
            product['carbs'] = float(tds[4].text.strip())
        except ValueError:
            continue  # skip the product if any of the values aren't present
        page_products.append(product)

    return page_products


def main(responses, filename='products'):
    """Gather results of every page and write them into a file."""
    result = []

    for r in responses:
        page_products = get_page_products(r)
        result.extend(page_products)

    with open(f'{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


if __name__ == '__main__':
    start = time.perf_counter()
    print('Collecting responses -->')
    responses = asyncio.run(await_responses(URLS))
    mid = time.perf_counter()
    print(f'ready in {(mid - start):.2f}s, parsing...')
    main(responses)
    end = time.perf_counter()
    print(f'Done in {(end - start):.2f}s')
