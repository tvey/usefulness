import datetime


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
