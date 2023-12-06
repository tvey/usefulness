"""Получаем число прописью.
Опционно можно передать единицу измерения.
Число может быть с дробной частью и отрицательными.
Результат — только количественное числительное.
"""


def handle_initial_value(value: float | int | str) -> dict:
    """"""
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
    integer = int(number - fractional_part)
    integer_parts = [int(i) for i in f'{integer:,}'.split(',')]

    return {
        'integer_parts': integer_parts,
        'fractional_part': fractional_part * 100,
        'is_negative': is_negative,
    }


def convert_thousands(value: int, position) -> str:
    """"""
    if not value:
        return ''


def get_number_in_words(
    value: float | int | str,
    integer_noun: str = '',
    fractional_noun: str = '',
    # round_up: bool = True,
) -> str:
    """"""
    number_info = handle_initial_value(value)

    if number_info['fractional_part']:
        pass

    for i, part in enumerate(number_info['integer_parts']):
        convert_thousands(part, i)
