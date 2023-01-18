import datetime
from zoneinfo import ZoneInfo


def unix_timestamp_to_iso_8601(timestamp: int, tz='localtime') -> str:
    seconds = timestamp / 1000
    return datetime.datetime.fromtimestamp(seconds, tz=ZoneInfo(tz)).isoformat()
