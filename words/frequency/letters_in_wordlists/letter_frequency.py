from collections import Counter

import pandas as pd


def get_wordlist_ru():
    """
    Get letter frequencies for Russian alphabet as percentages.

    Use this word frequency dictionary (csv version) to get the result:
    http://dict.ruslang.ru/freq.php
    """
    freq_df = pd.read_csv('wordlist_ru.csv', delimiter='\t')
    words = freq_df['Lemma'].values.tolist()
    return words


def get_wordlist_en():
    """
    Get letter frequencies for English alphabet as percentages.

    Use this word frequency list:
    https://www.kaggle.com/datasets/rtatman/english-word-frequency
    (the same as https://norvig.com/ngrams/count_1w.txt)
    """
    freq_df = pd.read_csv('wordlist_en.csv')
    words = freq_df['word'].values.tolist()
    return words


def get_letter_frequency(wordlist):
    if not wordlist:
        raise ValueError('A list of strings is required')

    letter_counter = Counter()

    for word in wordlist:
        letters = [i.lower() for i in str(word) if i.isalpha()]
        letter_counter.update(letters)

    total_letter_count = sum(letter_counter.values())
    frequencies = {}

    for t in letter_counter.most_common():
        letter_frequency = round((t[1] / total_letter_count) * 100, 2)
        frequencies[t[0]] = letter_frequency

    print('\n'.join(f'{k}: {v}%' for k, v in frequencies.items()))
    assert round(sum(frequencies.values())) == 100
    return frequencies
