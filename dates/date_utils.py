import datetime
from zoneinfo import ZoneInfo

from dateutil import parser


def get_date_difference(d1: str, d2: str, seconds=False):
    dt1 = parser.parse(d1)
    dt2 = parser.parse(d2)
    result = 0

    if dt1 > dt2:
        result = dt1 - dt2
    else:
        result = dt2 - dt1

    if seconds:
        return result.total_seconds()
    return result.days


def unix_timestamp_to_iso_8601(timestamp, tz='localtime'):
    seconds = timestamp / 1000
    return datetime.datetime.fromtimestamp(seconds, tz=ZoneInfo(tz)).isoformat()
