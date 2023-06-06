import datetime


def find_first_weekday(date: str, is_monday: bool = True) -> datetime.date:
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    if not is_monday:
        sunday = date_obj - datetime.timedelta(days=date_obj.weekday() + 1)
        return sunday
    else:
        monday = date_obj - datetime.timedelta(days=date_obj.weekday())
        return monday
