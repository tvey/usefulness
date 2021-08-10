import csv
import random
from datetime import date, timedelta

from structures import PRODUCTS, CATEGORIES

dates = [date(2020, 1, 1) + timedelta(days=d) for d in range(366)]


def add_bills_expenses(bills_data, date) -> list:
    bills_expenses = []

    for product, price in bills_data.items():
        bills_expenses.append((date, 'bills', product, price))

    return bills_expenses


def get_day_expenses(date) -> list:
    """In .csv product becomes description, price becomes (expense) amount."""
    day_expenses = []
    num_expenses = random.randint(2, 5)
    date_str = date.strftime('%Y-%m-%d')

    # add all bills expenses if date is the 1st day
    if date.day == 1:
        day_expenses += add_bills_expenses(CATEGORIES['bills'], date_str)

    expense_choices = [p for p in PRODUCTS if p['category'] != 'bills']

    for _ in range(num_expenses):
        expense_choice = random.choice(expense_choices)
        new_expense = (
            date_str,
            expense_choice['category'],
            expense_choice['product'],
            expense_choice['price'],
        )
        day_expenses.append(new_expense)

    print(day_expenses)

    return day_expenses


def write_expenses() -> None:
    fieldnames = ['date', 'category', 'description', 'amount']

    with open('../expenses.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(fieldnames)

        for d in dates:
            day_expenses = get_day_expenses(d)
            for row in day_expenses:
                writer.writerow(row)


if __name__ == '__main__':
    write_expenses()
