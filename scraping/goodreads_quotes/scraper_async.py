"""Scrape “Popular Quotes” on Goodreads using Requests-HTML; async version."""

import time
import json
import random
import asyncio

from requests_html import AsyncHTMLSession

BASE_URL = 'https://www.goodreads.com/quotes'
NUM_PAGES = 100
URLS = [f'{BASE_URL}?page={i}' for i in range(1, (NUM_PAGES + 1))]


async def get_response(asession, url):
    """Get url with async session and return the HTMLResponse."""
    r = await asession.get(url)

    sleep_time = random.random() * 2
    await asyncio.sleep(sleep_time)
    return r


async def await_responses(urls):
    """Gather tasks for event loop.
    A list of results will be returned *in order* thanks to asyncio.gather()
    """
    asession = AsyncHTMLSession()
    tasks = (get_response(asession, url) for url in urls)
    return await asyncio.gather(*tasks)


def get_page_quotes(r):
    """Collect quotes from a given page and return them as a list of dicts."""
    print(r.url)
    quote_elems = r.html.find('.quote')
    page_quotes = []

    for quote_elem in quote_elems:
        quote_text_raw = quote_elem.find('.quoteText', first=True)
        quote_text = quote_text_raw.text.split('”\n― ')[0].strip(' “')
        author = quote_elem.find('.authorOrTitle', first=True).text.strip(' ,')
        tags = [a.text for a in quote_elem.find('.smallText.left a')]
        quote = {
            'quote': quote_text,
            'author': author,
            'tags': tags,
        }
        page_quotes.append(quote)

    return page_quotes


def main(responses, filename='quotes'):
    """Gather results of every page and write them into a file."""
    result = []

    for r in responses:
        page_quotes = get_page_quotes(r)
        result.extend(page_quotes)

    with open(f'{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result


if __name__ == '__main__':
    start = time.perf_counter()
    print('Collecting responses -->')
    responses = asyncio.run(await_responses(URLS))
    mid = time.perf_counter()
    print(f'ready in {(mid - start):.2f}s, parsing...')
    main(responses, filename='quotes_async')
    end = time.perf_counter()
    print(f'Done in {(end - start):.2f}s')
