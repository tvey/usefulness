from collections import Counter

import pandas as pd


def get_letter_frequency_ru():
    """
    Get letter frequencies for Russian alphabet as percentages.

    Use the word frequency dictionary to get the result:
    http://dict.ruslang.ru/freq.php

    Mb use this dict: http://opencorpora.org/?page=downloads
    """
    freq_df = pd.read_csv('freqrnc2011.csv', delimiter='\t')
    words = freq_df['Lemma'].values.tolist()
    letter_counter = Counter()

    for word in words:
        letters = [i.lower() for i in word if i.isalpha()]
        letter_counter.update(letters)

    total_letter_count = sum(letter_counter.values())
    frequencies = {}

    for t in letter_counter.most_common():
        letter_frequency = round((t[1] / total_letter_count) * 100, 2)
        frequencies[t[0]] = letter_frequency

    print('\n'.join(f'{k}: {v}%' for k, v in frequencies.items()))
    assert round(sum(frequencies.values())) == 100
    return frequencies


def get_letter_frequency_en():
    """
    Get letter frequencies for English alphabet as percentages.

    Use this word frequency list for now:
    https://www.kaggle.com/datasets/rtatman/english-word-frequency
    """
    freq_df = pd.read_csv('unigram_freq.csv')
    words = freq_df['word'].values.tolist()
    letter_counter = Counter()

    for word in words:
        letter_counter.update(list(str(word)))

    total_letter_count = sum(letter_counter.values())
    frequencies = {}

    for t in letter_counter.most_common():
        letter_frequency = round((t[1] / total_letter_count) * 100, 2)
        frequencies[t[0]] = letter_frequency

    print('\n'.join(f'{k}: {v}%' for k, v in frequencies.items()))
    assert round(sum(frequencies.values())) == 100
    return frequencies
