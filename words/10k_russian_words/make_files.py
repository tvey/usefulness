"""Making usable files out of a word list spreadsheet from this Reddit post:
https://www.reddit.com/r/russian/comments/289wba/

The spreadsheet is saved as a csv file to make it easier to use.

The original spreadsheet is based on a book
https://www.amazon.com/Russian-Learners-Dictionary-Words-Frequency/dp/0415137926
"""

import csv
import json
import os
import re

os.chdir('words')


def format_csv(orig_csv, out_csv):
    with open(orig_csv, encoding='utf-8') as f:
        reader = csv.reader(f)
        with open(out_csv, 'w', encoding='utf-8', newline='') as new_file:
            writer = csv.writer(new_file, quoting=csv.QUOTE_ALL)
            writer.writerow(['ru', 'forms', 'en', 'example_ru', 'example_en'])
            for row in reader:
                ru = re.split(r'\W+', row[0])[0]
                forms = row[0].split(ru, 1)[1].strip()
                examples = row[2].split('|')
                new_row = [ru, forms, row[1]] + examples
                writer.writerow(new_row)


def make_json(csv_file, json_file):
    with open(csv_file, encoding='utf-8') as f:
        csv_rows = []
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        for row in reader:
            elem = {fields[i]: row[fields[i]] for i in range(len(fields))}
            csv_rows.append(elem)
        with open(json_file, 'w', encoding='utf-8') as new_file:
            new_file.write(
                json.dumps(
                    csv_rows,
                    indent=4,
                    ensure_ascii=False,
                    sort_keys=False,
                    separators=(',', ': '),
                )
            )


def make_txt(csv_file, txt_file):
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        words = [row[0] for row in reader]

        with open(txt_file, 'w', encoding='utf-8') as new_file:
            new_file.write('\n'.join(words) + '\n')


def main():
    orig_csv = '10000 most common russian words.csv'
    csv_10k = '10k_words.csv'
    json_10k = '10k_words.json'
    txt_10k = '10k_words.txt'

    format_csv(orig_csv, csv_10k)
    make_json(csv_10k, json_10k)
    make_txt(csv_10k, txt_10k)


if __name__ == '__main__':
    main()
