from datetime import datetime, date, timedelta


def get_week_number_from_date(date: str) -> int:
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    year, week, weekday = date_obj.isocalendar()
    return week


def get_dates_from_week_number(week_number: int, year: int) -> list[date, date]:
    monday = datetime.strptime(f'{year}-{week_number:02}-1', '%Y-%W-%w').date()
    sunday = monday + timedelta(days=6)
    return monday, sunday
