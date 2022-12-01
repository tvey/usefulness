import random
import pymorphy2

PARTS_OF_SPEECH = {
    'ADJF': '',
    'ADJS': '',
    'ADVB': '',
    'COMP': '',
    'CONJ': '',
    'GRND': '',
    'INFN': '',
    'INTJ': '',
    'NOUN': '',
    'NPRO': '',
    'NUMR': '',
    'PRCL': '',
    'PRED': '',
    'PREP': '',
    'PRTF': '',
    'PRTS': '',
    'VERB': '',
}


def get_random_word():
    with open('words_ru.txt') as f:
        words = f.read().split('\n')

    return random.choice(words)


word = get_random_word()

morph = pymorphy2.MorphAnalyzer()

p = morph.parse(word)[0]
part_of_speech = str(p.tag).split(',')[0]
print(f'{word}: {part_of_speech}')
