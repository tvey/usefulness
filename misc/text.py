import re
from collections import Counter

from nltk.corpus import stopwords


def count_words(file_path: str) -> list[tuple]:
    with open(file_path) as f:
        text = f.read()

    words = re.findall(r'\w+', text.lower())
    return Counter(words).most_common()


def remove_stopwords(words: list) -> list:
    return [i for i in words if i[0] not in stopwords.words('english')]
