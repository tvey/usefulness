"""Scrape the “Best Books Ever” list on Goodreads."""

import time
import json
import random
import asyncio

from requests_html import AsyncHTMLSession, HTMLResponse

BASE_URL = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'
NUM_PAGES = 10
URLS = [f'{BASE_URL}?page={i}' for i in range(1, (NUM_PAGES + 1))]


async def get_response(asession: AsyncHTMLSession, url: str) -> HTMLResponse:
    """Get url with async session and return the HTMLResponse."""
    r = await asession.get(url)
    sleep_time = random.random() * 2
    await asyncio.sleep(sleep_time)
    return r


async def await_responses(urls: list[str]):
    """Gather tasks for event loop.
    A list of results will be returned *in order* thanks to asyncio.gather()
    """
    asession = AsyncHTMLSession()
    tasks = (get_response(asession, url) for url in urls)
    return await asyncio.gather(*tasks)


def get_page_books(r: HTMLResponse) -> list:
    """Collect books meta from a page and return them as a list of dicts."""
    table = r.html.find('.tableList', first=True)
    rows = table.find('tr')
    books = []

    for row in rows:
        rank = row.find('td', first=True).text
        url = list(row.find('td')[1].absolute_links)[0]
        cover_url = row.find('img', first=True).attrs['src']
        info = row.find('td')[2]
        title = info.find('.bookTitle', first=True).text
        author = info.find('.authorName', first=True).text
        rating = info.find('.minirating', first=True).text
        rating = rating.removeprefix('it was amazing').removeprefix('really liked it')
        avg, ratings = rating.split(' — ')
        avg_ratings = float(avg.strip().split(' ')[0])
        num_ratings = int(ratings.split(' ')[0].replace(',', ''))
        score_info = info.find('.smallText > a')
        score = score_info[0].text.split('score: ')[1]
        votes = int(score_info[1].text.split(' ')[0].replace(',', ''))

        book = {
            'rank': rank,
            'title': title,
            'author': author,
            'url': url,
            'cover_url': cover_url,
            'avg_rating': avg_ratings,
            'num_ratings': num_ratings,
            'score': score,
            'votes': votes,
        }
        books.append(book)

    return books


def main(responses: list[HTMLResponse], filename: str = 'list') -> list:
    """Gather results of every page and write them into a file."""
    result = []

    for r in responses:
        print(r.url)
        page_quotes = get_page_books(r)
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
    main(responses)
    end = time.perf_counter()
    print(f'Done in {(end - start):.2f}s')
