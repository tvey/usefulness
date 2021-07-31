"""Scrape “Popular Quotes” on Goodreads using Requests-HTML; sync version."""

import json
import time
import random

from requests_html import HTMLSession

BASE_URL = 'https://www.goodreads.com/quotes'
NUM_PAGES = 100
URLS = [f'{BASE_URL}?page={i}' for i in range(1, (NUM_PAGES + 1))]


def get_page_quotes(session, url):
    """Collect quotes from a given page and return them as a list of dicts."""
    r = session.get(url)
    print(url)
    quote_elems = r.html.find('.quote')
    page_quotes = []

    for quote_elem in quote_elems:
        quote_text_raw = quote_elem.find('.quoteText', first=True)
        quote = quote_text_raw.text.split('”\n― ')[0].strip(' “')
        author = quote_elem.find('.authorOrTitle', first=True).text.strip(' ,')
        tags = [a.text for a in quote_elem.find('.smallText.left a')]
        result = {
            'quote': quote,
            'author': author,
            'tags': tags,
        }
        page_quotes.append(result)

    return page_quotes


def main(urls, filename='quotes'):
    """Gather results of every page and write them into a file."""
    session = HTMLSession()
    result = []
    start = time.perf_counter()

    for i, url in enumerate(urls, start=1):
        page_quotes = get_page_quotes(session, url)
        result.extend(page_quotes)
        time.sleep(random.random() * 2)

    with open(f'{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    end = time.perf_counter()
    print(f'Done in {(end - start):.2f}s')

    return result


if __name__ == '__main__':
    main(URLS)
