import random
import string

DEFAULT_CHARS = string.ascii_letters + string.digits


def calculate_combinations(length: int, chars: str = DEFAULT_CHARS) -> int:
    """Get a number of possible combinations of chars for a specified length."""
    unique_chars_count = len(set(chars))
    return unique_chars_count**length


def generate_short_code(length: int, chars: str = DEFAULT_CHARS) -> str:
    """Generates a random short code of the specified length."""
    return ''.join(random.choice(chars) for _ in range(length))


def is_unique(code: str, existing_codes: set) -> bool:
    """Checks if the given code is unique in the set of existing codes."""
    return code not in existing_codes


def generate_unique_codes(
    count: int,
    length: int,
    existing_codes: set,
    chars: str = DEFAULT_CHARS,
) -> set:
    """Generates multiple short codes of a given length with no duplicates."""
    unique_codes = set()
    while len(unique_codes) < count:
        new_code = generate_short_code(length, chars)
        if is_unique(new_code, existing_codes):
            unique_codes.add(new_code)
    return unique_codes


if __name__ == '__main__':
    lengths = range(3, 8)
    for i in lengths:
        combinations = f'{calculate_combinations(i):_}'.replace('_', ' ')
        print(f'Length {i}: {combinations}')
        print(f'Example code: {generate_short_code(i)}')
