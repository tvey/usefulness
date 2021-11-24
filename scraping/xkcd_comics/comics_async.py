"""Probably you want to have all the xkcd comics locally.
Async version, so it's lightning-fast.
"""

import asyncio
import os
import random
import re
import sys
import time
from urllib.parse import urljoin

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = 'https://xkcd.com/'


async def get_latest_comic(session):
    async with session.get(BASE_URL) as r:
        assert r.status == 200
        html = await r.text()
        soup = BeautifulSoup(html, 'html.parser')
        prev_link = soup.select('.comicNav > li:nth-child(2) > a')[0]
        prev = prev_link.attrs['href'].strip('/')
        latest = int(prev) + 1
        print(f'Latest comic: {latest}')
        return latest


async def get_single_comic_data(session, num):
    async with session.get(f'{BASE_URL}{num}', ssl=False) as r:
        html = await r.text()
        sleep_time = random.random() * 3
        await asyncio.sleep(sleep_time)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('div', id='ctitle').text
        p = r'Permanent link to this comic: <a href="https://xkcd.com/(\d+)">'
        match = re.search(p, html)
        if match:
            num = int(match.group(1))
        image_elem = soup.select('#comic img')[0]
        rel_image_src = image_elem.attrs['src']
        image_src = urljoin(BASE_URL, rel_image_src)
        if image_elem.attrs.get('srcset'):
            rel_image_src = image_elem.attrs['srcset'].strip(' 2x')
            image_src = urljoin(BASE_URL, rel_image_src)
        ext = os.path.splitext(image_src)[-1]
        forbidden_chars = '\\/:*?"<>|%.,;= '
        table = str.maketrans(forbidden_chars, '_' * len(forbidden_chars))
        filename_title = title.translate(table).strip('_').replace('__', '_')
        filename = f"{num:>04d}_{filename_title}{ext}"

        print(f'Data ready: {num}. {title}')
        return {
            'id': num,
            'title': title,
            'filename': filename,
            'image_src': image_src,
        }


async def get_comic_data(session, latest, start=1):
    non_typical = [404, 961, 1037, 1116, 1264, 1350, 1416, 1608, 1663, 2198]
    tasks = []

    for num in range(start, latest + 1):
        if num in non_typical:
            continue
        tasks.append(asyncio.create_task(get_single_comic_data(session, num)))

    return await asyncio.gather(*tasks)


async def get_image(session, single_comic_data):
    data = single_comic_data
    async with session.get(data['image_src'], ssl=False) as r:
        sleep_time = random.random() * 3
        await asyncio.sleep(sleep_time)
        if r.status == 200:
            f = await aiofiles.open(f"comics/{data['filename']}", mode='wb')
            await f.write(await r.read())
            await f.close()
            print(f"Image ready: {data['id']}. {data['title']}")


async def get_all_images(session, comic_data):
    tasks = []

    for d in comic_data:
        tasks.append(asyncio.create_task(get_image(session, d)))
    return await asyncio.gather(*tasks)


def get_latest_downloaded():
    """Number of the latest downloaded image in comics/ from current folder."""
    try:
        files = sorted([f for f in os.listdir('comics') if f.endswith('png')])
        latest = files[-1].split('_', 1)[0]
        return int(latest)
    except FileNotFoundError:
        print('No comics/ folder here. Downloading everything.')
        return


async def main():

    async with aiohttp.ClientSession() as session:
        latest = await get_latest_comic(session)
        ld = get_latest_downloaded()

        if ld == latest:
            print('Latest comic is already downloaded.')
            return
        elif not ld:
            comic_data = await get_comic_data(session, latest)
        else:
            comic_data = await get_comic_data(session, latest, start=(ld + 1))

        os.makedirs('comics', exist_ok=True)
        await get_all_images(session, comic_data)


if __name__ == '__main__':
    start = time.perf_counter()
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end = time.perf_counter()
    print(f'Done in {(end - start):.0f} seconds')
