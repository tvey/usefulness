import csv
import random


with open('extra/stressed_simplified.csv', encoding='utf-8') as f:
    stressed = list(csv.DictReader(f))

    random_row = random.choice(stressed)
    word = random_row['word']
    idx = int(random_row['stressed_letter_index'])
    display_word = ''

    if idx != -1:
        display_word = word[:idx] + word[idx].upper() + word[idx + 1 :]
        assert word[idx] == random_row['stressed_letter']
    else:
        display_word = word
    print(display_word)
