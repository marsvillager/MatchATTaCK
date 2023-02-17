from nltk.corpus import wordnet as wn
from security_rules.process.process_data import process
from tools.transform import is_lemma


def match_synset(keyword: str) -> set[str]:
    """
    Word representation depends on knowledge.

    :param keyword: keyword to match
    :return: set of synonyms of keyword
    """
    words: list[str] = []
    for synset in wn.synsets(keyword):
        for word in synset.lemmas():
            if '_' not in word.name():
                words.append(word.name())

    return set(words)


def get_synset(filename: str, lemma: bool) -> set[str]:
    """
    Word representation depends on knowledge.

    :param filename: security files
    :param lemma: word ==> lemma if True, stay the same if False
    :return: keywords and its synonyms
    """
    keywords: set[str] = process(filename, False)  # no lemma

    word_list: str = ' '.join(keywords) + ' '
    for keyword in keywords:
        word_list = word_list + ' '.join(match_synset(keyword))  # match synonyms

    return is_lemma(word_list, lemma)  # lemma
