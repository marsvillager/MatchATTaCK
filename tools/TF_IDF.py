from collections import Counter

from nltk import FreqDist

from tools.transform import freq_count


class TfIdf:
    def __init__(self):
        self.words = list[str]
        self.words_all = list[str]

        self.term = FreqDist()
        self.term_num = 0

        self.doc_num = 0
        self.term_all = FreqDist()

    def setter(self, words, doc_num, words_all):
        self.words = words
        self.doc_num = doc_num
        self.words_all = words_all

        self.term = freq_count(self.words)
        self.term_num = len(self.words)
        self.term_all = freq_count(self.words_all)
