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


def unix_timestamp_to_iso_8601(timestamp: int, tz='localtime') -> str:
    seconds = timestamp / 1000
    return datetime.datetime.fromtimestamp(seconds, tz=ZoneInfo(tz)).isoformat()


def get_age(date_of_birth: str) -> int:
    """Get age as full years."""
    today = datetime.date.today()

    try:
        dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    except ValueError:
        raise ValueError('Enter a valid date in format DD-MM-YYYY.')

    if dob > today:
        raise ValueError('Date of birth cannot be later than today.')

    age = int((today - dob).days // 365.2425)

    if dob.day == today.day and dob.month == today.month and age > 0:
        age += 1

    return age
