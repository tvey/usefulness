import json

from requests_html import HTMLSession

URL = 'https://rsport.ria.ru/20220514/kaloriynost-1788483172.html'


def get_products():
    s = HTMLSession()
    r = s.get(URL)
    tables = r.html.find('table')
    rows = [row for table in tables for row in table.find('tr')[1:]]
    products = []

    for row in rows:
        prod = {}
        tds = row.find('td')
        prod['name'] = tds[0].text
        macros = [float(tds[i].text.replace(',', '.')) for i in range(1, 5)]
        prod['prot'], prod['fat'], prod['carbs'], prod['cals'] = macros
        products.append(prod)

    return products


def main():
    products = get_products()

    with open('ria_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
