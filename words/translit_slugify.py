"""
Example of a common-sense Cyrillic (Russian) -> Latin transliteration.
May be useful for URLs and other paths.
"""

import re

TRANSLIT_MAP = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': 'y',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}


def translit(value):
    for v in [('ый', 'y'), ('ЫЙ', 'Y')]:
        value = re.sub(v[0], v[1], value)

    transliterated_value = [
        TRANSLIT_MAP.get(i.lower(), i).upper()
        if i.isupper()
        else TRANSLIT_MAP.get(i, i)
        for i in value
    ]
    return ''.join(transliterated_value).strip()


def slugify(value):
    # Django's slugify substitutions
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s]+', '-', value).lower()


def translit_slugify(value):
    return slugify(translit(value))


sentence = 'Шифровальщица попросту забыла ряд ключевых множителей и тэгов.'
print(translit_slugify(sentence))

title = 'Миндальный торт с клубникой и яблоками без выпечки'
print(translit_slugify(title))

другой_заголовок = '80 вещей, которые нужно успеть сделать до 80 лет'
print(translit_slugify(другой_заголовок))
