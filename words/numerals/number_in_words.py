"""Получаем число прописью.
Есть возможность передать единицу измерения.
Число может быть с дробной частью и отрицательным.
Дробная часть будет округлена до сотых.
Результат — только количественное числительное.
"""
import pymorphy2  # up to python 3.10

from constants import numerals, orders


def handle_initial_value(value: float | int | str) -> dict:
    """Create info about the value."""
    if isinstance(value, str) and ',' in value:
        value = value.replace(',', '.')

    try:
        number = float(value)
    except ValueError:
        raise ValueError(f'Incorrect input value: {value}')

    is_negative = number < 0
    fractional_part = 0
    if not number.is_integer() or number < 10**9:
        fractional_part = round(number % 1, 2)
    integer = abs(int(number - fractional_part))
    integer_parts = [int(i) for i in f'{integer:,}'.split(',')]

    return {
        'integer_parts': integer_parts,
        'fractional_part': fractional_part * 100,
        'is_negative': is_negative,
    }


def make_agree(word: str, number: int):
    """Make an appropriate form of the word following the number."""
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    order_morph = morph.parse(word)[0]
    return order_morph.make_agree_with_number(number).word


def convert_part(num: int, position: int) -> str:
    """Make words from a less-than-1000 part of the split number."""
    if not num:
        return ''

    hundreds, rest = (num - num % 100), num % 100
    if rest > 20:
        tens = rest - rest % 10
        units = num - hundreds - tens
        values = [hundreds, tens, units]
    else:
        values = [hundreds, 0, rest]

    order = ''
    last_num = values[-1]

    if position == -2:  # for fractional
        pass
    elif position == -1:  # below 1000
        order = ''
    else:
        order = make_agree(orders[position], last_num)

    text_nums = [numerals.get(i) for i in values if i]
    if position == 0 and last_num in [1 + j for j in range(0, 100, 10)]:
        text_nums[-1] = 'одна'
    elif position == 0 and last_num in [2 + j for j in range(0, 100, 10)]:
        text_nums[-1] = 'две'

    text_value = ' '.join(text_nums)
    if order:
        return f'{text_value} {order}'
    return text_value


def get_number_in_words(
    value: float | int | str,
    integer_noun: str = '',
    fractional_noun: str = '',
) -> str:
    """"""
    number_info = handle_initial_value(value)

    # handle zero

    if number_info['fractional_part']:
        frac_part = convert_part(number_info['fractional_part'], -2)  # finish

    converted_parts = []

    for i, part in enumerate(number_info['integer_parts'][::-1], -1):  # reverse
        part_text = convert_part(part, i)
        converted_parts.append(part_text)

    result_parts = [i for i in converted_parts[::-1] if i]
    print(f'{value:_}')
    print(' '.join(result_parts))


if __name__ == '__main__':
    get_number_in_words(1000022302)
