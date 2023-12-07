import datetime

from dateutil import relativedelta


def validate_date(d):
    try:
        return datetime.datetime.strptime(d, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Enter a valid date in format DD-MM-YYYY.')


def get_date_difference(d1: str, d2: str, seconds=False) -> int:
    """Input dates are expected to have format DD-MM-YYYY"""
    dt1, dt2 = validate_date(d1), validate_date(d2)
    result = 0

    if dt1 > dt2:
        result = dt1 - dt2
    else:
        result = dt2 - dt1

    if seconds:
        return result.total_seconds()
    return result.days


def get_difference_in_var_units(start_date: str, end_date: str = '') -> dict:
    start = validate_date(start_date)

    if end_date:
        end = validate_date(end_date)
    else:
        end = datetime.datetime.today().date()

    days = abs((end - start).days)

    return {
        'weeks': days // 7,
        'days': days,
        'hours': days * 24,
        'minutes': days * 24 * 60,
        'seconds': days * 24 * 60 * 60,
    }


# def get_difference_with_relativedelta(d1: str, d2: str) -> dict:
#     dt1, dt2 = validate_date(d1), validate_date(d2)
#     rd = relativedelta.relativedelta(dt1, dt2)

#     return {
#         'years': rd.years,
#         'months': rd.months,
#         'days': rd.days,
#     }
