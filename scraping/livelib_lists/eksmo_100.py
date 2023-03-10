import json

import requests
from bs4 import BeautifulSoup


def scrape():
    base_url = 'https://www.livelib.ru/pubseries/34817-100-glavnyh-knig/~'
    urls = [f'{base_url}{i}' for i in range(1, 8)]
    result = []

    for url in urls:
        r = requests.get(url)
        r.encoding = 'utf-8'  #
        soup = BeautifulSoup(r.text, 'html.parser')
        booklist = soup.find(id='booklist')
        cards = booklist.find_all('div', {'class': 'card-block'})

        for card in cards:
            book = {}
            number = card.find(True, {'class': 'brow-topno'}).get_text()
            book['number'] = int(number[1:])
            title = card.find('a', {'class': 'brow-book-name'}).get_text()
            book['title'] = title
            isbn = card.find('span', attrs={'itemprop': 'isbn'}).get_text()  #
            book['isbn'] = isbn
            author = card.find('a', {'class': 'brow-book-author'})
            try:
                book['author'] = author.get_text()
            except AttributeError:
                book['author'] = ''
            result.append(book)

    with open('eksmo_100.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
