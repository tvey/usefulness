import os
from html.parser import HTMLParser

import ebooklib
from ebooklib import epub


class Parser(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


def epub_to_txt(epub_path):
    filename = os.path.basename(epub_path)
    name = os.path.splitext(filename)[0]
    book = epub.read_epub(epub_path)
    text = ''

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_body_content().decode()
            parser = Parser()
            parser.feed(content)
            text += parser.text.strip().replace('\xa0', ' ')

    new_filename = f'{name}.txt'

    with open(new_filename, 'w') as f:
        f.write(text)

    print(f'File created: {new_filename}')
