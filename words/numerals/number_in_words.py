"""Получаем число прописью.
Есть возможность передать единицу измерения.
Число может быть с дробной частью и отрицательным.
Дробная часть будет округлена до сотых.
Результат — только количественное числительное.
"""
import pymorphy2  # up to python 3.10

from constants import numerals, orders

morph = pymorphy2.MorphAnalyzer(lang='ru')


def handle_initial_value(value: float | int | str) -> dict:
    """Create info about the value."""
    if isinstance(value, str) and (',' in value or ' ' in value):
        value = value.replace(',', '.').replace(' ', '')

    try:
        number = float(value)
    except ValueError:
        raise ValueError(f'Incorrect input value: {value}')

    is_negative = number < 0
    number = abs(number)
    fractional_part = 0
    if not number.is_integer() and number < 10**9:
        fractional_part = round(number % 1, 2)
    integer = int(number - fractional_part)
    integer_parts = [int(i) for i in f'{integer:,}'.split(',')]

    return {
        'number': float(value),
        'integer_parts': integer_parts,
        'fractional_part': int(fractional_part * 100),
        'is_negative': is_negative,
    }


def normalize_word(word: str) -> str:
    """Make sure the word is in a base form for correct pymorphy2 handling."""
    return morph.parse(word)[0].normal_form


def match_num_and_noun(num: int, num_in_words: str, noun: str) -> str:
    """Make an appropriate form of the word following the number."""
    forms = {'femn': {1: 'одна', 2: 'две'}, 'neut': {1: 'одно'}}
    word_morph = morph.parse(noun)[0]
    matched_word = word_morph.make_agree_with_number(num).word
    word_gender = word_morph.tag.gender
    non_hundreds_part = num % 100
    ends_1_2 = [1, 2] + [i + j for i in [1, 2] for j in range(20, 100, 10)]

    if non_hundreds_part in ends_1_2:
        if word_gender and word_gender in ['femn', 'neut']:
            form = forms.get(word_gender, {}).get(num)
            num_in_words = ' '.join(num_in_words.split(' ')[:-1] + [form])

    return f'{num_in_words} {matched_word}'


def convert_part(num: int, noun: str = '') -> str:
    if not num:
        return ''

    hundreds, rest = (num - num % 100), num % 100
    if rest > 20:
        tens = rest - rest % 10
        units = num - hundreds - tens
        values = [hundreds, tens, units]
    else:
        values = [hundreds, 0, rest]

    words = [numerals.get(i) for i in values if i]
    num_in_words = ' '.join(words)

    if noun:
        num_in_words = match_num_and_noun(num, num_in_words, noun)

    return num_in_words


def get_number_in_words(
    value: float | int | str,
    int_noun: str = '',
    frac_noun: str = '',
) -> str:
    """"""
    if not value:
        return convert_part(0, int_noun)
    info = handle_initial_value(value)
    integer_parts, frac_part = info['integer_parts'], info['fractional_part']
    converted_parts = []

    for order, part in enumerate(integer_parts[::-1], -1):
        if order >= 0:
            order_noun = orders[order]
            part_text = convert_part(part, order_noun)
        elif int_noun:
            part_text = convert_part(part, normalize_word(int_noun))
        else:
            part_text = convert_part(part)
        converted_parts.append(part_text)

    number_in_words = ' '.join([i for i in converted_parts[::-1] if i])

    if frac_part:
        frac_in_words = convert_part(frac_part, normalize_word(frac_noun))
        if not int_noun:
            number_in_words = f'{number_in_words} целых {frac_in_words}'.strip()
        else:
            number_in_words = f'{number_in_words} {frac_in_words}'.strip()


    if info['is_negative']:
        number_in_words = f'минус {number_in_words}'

    print(f'{info["number"]:_}:', number_in_words)
    return number_in_words


if __name__ == '__main__':
    get_number_in_words(33, 'корова')
    get_number_in_words(321000122.12, 'рубль', 'копейка')
    get_number_in_words(-121349900.12, 'доллары', 'центы')
    get_number_in_words('0.12345', frac_noun='долей')
    get_number_in_words('123 345,678')
