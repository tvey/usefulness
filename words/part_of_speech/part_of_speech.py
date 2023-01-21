import random
import pymorphy2

PARTS_OF_SPEECH = {
    'ADJF': 'adjective (full)',
    'ADJS': 'adjective (short)',
    'ADVB': 'adverb',
    'COMP': 'comparative',
    'CONJ': 'conjunction',
    'GRND': 'transgressive',
    'INFN': 'verb (infinitive)',
    'INTJ': 'interjection',
    'NOUN': 'noun',
    'NPRO': 'pronoun',
    'NUMR': 'numeral',
    'PRCL': 'particle',
    'PRED': 'predicative',
    'PREP': 'preposition',
    'PRTF': 'participle (full)',
    'PRTS': 'participle (short)',
    'VERB': 'verb',
}


def get_random_word():
    with open('words_en.txt') as f:
        words = f.read().split('\n')

    return random.choice(words)


word = get_random_word()

morph = pymorphy2.MorphAnalyzer()

p = morph.parse(word)[0]
part_of_speech = str(p.tag).split(',')[0]
print(f'{word}: {PARTS_OF_SPEECH.get(part_of_speech)}')
