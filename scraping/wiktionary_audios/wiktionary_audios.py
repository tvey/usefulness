import os
import urllib.parse

from requests_html import HTMLSession

wiki_langs = {
    'ru': 'https://ru.wiktionary.org/wiki/',
}

session = HTMLSession()


def get_random_word() -> str:
    import random

    with open('words.txt', encoding='utf-8') as f:
        words = [w for w in f.read().split('\n') if w]

    return random.choice(words)


def get_audio_pages(word: str, lang: str):
    url = f'{wiki_langs.get(lang)}{word}'
    r = session.get(url)
    audio_pages = [
        link for link in r.html.absolute_links if link.endswith('.ogg')
    ]
    if not audio_pages:
        print(f'No audios found for {word}')
        return []
    return audio_pages


def get_audio_file(audio_page: str, save_to: str):
    r = session.get(audio_page)
    audio = [
        urllib.parse.unquote(link, encoding='utf-8')
        for link in r.html.absolute_links
        if link.endswith('.ogg') and 'upload' in link
    ][0]
    filename = os.path.basename(audio).split('-', maxsplit=1)[-1]
    file_path = os.path.join(save_to, filename)
    print(file_path)
    r = session.get(audio)
    with open(file_path, 'wb') as f:
        f.write(r.content)


def get_audios(word, lang='ru', save_to='audios'):
    os.makedirs(save_to, exist_ok=True)

    audio_pages = get_audio_pages(word, lang)

    if audio_pages:
        for audio_page in audio_pages:
            get_audio_file(audio_page, save_to)


if __name__ == '__main__':
    word = get_random_word()
    get_audios(word)
