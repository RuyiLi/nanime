import csv
import re
from typing import List, Dict
from collections import Counter
from math import log

from unidecode import unidecode


class Anime:
    _raw: dict
    title: str
    genres: List[str]
    desc: str
    _raw_desc: str
    terms: List[str]
    freq: Counter

    weights: List

    def __init__(self, data: dict):
        self._raw = data

        self.title = data['Title']
        self.genres = data['Genres'].split(',')

        self.desc = data['Description']
        self._raw_desc = unidecode(self.desc).lower()
        self.terms = re.split(r'\W+', self._raw_desc)
        self.freq = Counter(self.terms)

        self.weights = []

    def augmented_freq(self, term: str):
        raw_frequency = self.freq[term]
        most_occurring_term = self.freq.most_common(1)[0][1]
        return 0.5 + 0.5 * raw_frequency / most_occurring_term


with open('dataanime.csv', encoding='utf-8') as source:
    reader = csv.DictReader(source)
    i = 0
    animes = [*map(Anime, reader)]
    N = len(animes)


def find_relevant(terms):
    for anime in animes:
        anime.weights = []

    for term in terms:
        term_frequency = sum((term in anime.terms) for anime in animes) + 1
        idf = log(N / term_frequency)

        for anime in animes:
            # tf = 0.5 + 0.5 * anime.freq[term] / anime.freq.most_common()[0][1]
            tf = log(1 + anime.freq[term])
            tf_idf = (tf * idf)
            anime.weights.append(tf_idf)

    def key(anime):
        try:
            return sum(anime.weights)
        except ZeroDivisionError:
            return 0

    res = sorted(animes, key=key, reverse=True)
    return res


if __name__ == '__main__':
    rel = find_relevant(input().lower().strip().split())
    for a in rel[:10]:
        print(a.__dict__)
