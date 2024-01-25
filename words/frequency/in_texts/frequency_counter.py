import re
from collections import Counter


def count_letters(text):
    letters = [i for i in text if i.isalpha()]
    return Counter(letters)


def count_bigrams(text):
    words = re.findall(r'\b\w+\b', text.lower())
    bigrams = []

    for i in range(len(words) - 1):
        bigrams.append(f'{words[i]} {words[i+1]}')

    return Counter(bigrams)


def analyze_text(text):
    counted_letters = count_letters(text)
    counted_bigrams = count_bigrams(text)
    print('Counted letters:', len(counted_letters))
    print('Counted bigrams:', len(counted_bigrams))

    for i in counted_letters.most_common(10):
        print(i)

    print('-' * 30)

    for i in counted_bigrams.most_common(100):
        print(i)


with open('идиот.txt') as f1, open('idiot.txt') as f2:
    text_1, text_2 = f1.read(), f2.read()

analyze_text(text_1)
