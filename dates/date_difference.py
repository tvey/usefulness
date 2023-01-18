import datetime
from zoneinfo import ZoneInfo


def get_date_difference(d1: str, d2: str, seconds=False) -> int:
    """Input dates are expected to have format DD-MM-YYYY"""
    try:
        dt1 = datetime.datetime.strptime(d1, '%d-%m-%Y')
        dt2 = datetime.datetime.strptime(d2, '%d-%m-%Y')
    except ValueError:
        raise ValueError('Enter a valid date in format DD-MM-YYYY.')

    result = 0

    if dt1 > dt2:
        result = dt1 - dt2
    else:
        result = dt2 - dt1

    if seconds:
        return result.total_seconds()
    return result.days
