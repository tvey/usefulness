from datetime import datetime, timedelta

date_formats = [
    '%Y-%m-%d',
    '%d-%m-%Y',
    '%d.%m.%Y',
    '%d-%m',
    '%m-%d',
    '%d.%m',
    '%m.%d',
]


def get_date_list(
    start: str,
    end: str,
    output_format: str = date_formats[2],
    include_end: bool = True,
    reverse: bool = False,
) -> list[str]:
    """Get a range of date strings between start and end."""
    try:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Dates must be valid and in format "%Y-%m-%d"')
    if start_date > end_date:
        raise ValueError('Make sure the end date is later than the start date')

    if include_end:
        end_date += timedelta(days=1)

    dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days)
    ]
    result = [datetime.strftime(date, output_format) for date in dates]
    if reverse:
        return result[::-1]
    return result


if __name__ == '__main__':
    dates = get_date_list('2024-02-01', '2024-03-01', output_format='%d.%m')
    assert '29.02' in dates
    assert '01.03' in dates
