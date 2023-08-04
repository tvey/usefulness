import re


def parse_file_size(size: str) -> int:
    """Convert human-readable file size string to bytes (factor of 1000)."""
    units = {
        'B': 1,
        'BYTES': 1,
        'KB': 1000,
        'MB': 1000**2,
        'GB': 1000**3,
        'TB': 1000**4,
    }
    size = size.strip().upper()

    if not 'B' in size or not any(i.isdigit() for i in size):
        raise ValueError('Make sure both unit and size are specified')
    elif size[-2:] not in units:
        raise ValueError('Check if the filesize unit is kB, MB, GB, or TB.')

    if not ' ' in size:
        size = re.sub(r'([KMGT]?B)', r' \1', size)

    number, unit = size.split()
    return int(float(number) * units[unit])


sizes = ['9 Gb', '100.1mb', '216.52 KB', '216.25kB', '  19.7GB ', '.9gb']

assert parse_file_size(sizes[0]) / 10 == parse_file_size(sizes[-1])
assert parse_file_size(sizes[1]) == 100100000
assert parse_file_size(sizes[0]) < parse_file_size(sizes[4])
assert parse_file_size(sizes[2]) > parse_file_size(sizes[3])
