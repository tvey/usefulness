import os

from bs4 import BeautifulSoup

highlights_file = 'kindle_highlights.html'

with open(highlights_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

highlights_elems = soup.find_all('div', {'class': 'noteText'})

if highlights_elems:
    name = os.path.basename(highlights_file).split('.')[0]

    with open(f'{name}.txt', 'w', encoding='utf-8') as ff:
        highlights = [h.text.strip() for h in highlights_elems]
        ff.write('\n\n'.join(highlights))
