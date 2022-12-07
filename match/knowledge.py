from nltk.corpus import wordnet as wn
from data.security_rules.process_data import process
from tools.config import Config
from tools.transform import stemmer


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


def get_synset(filename: str) -> set[str]:
    """
    Word representation depends on knowledge.

    :param filename: security files
    :return: set(lemma) of keywords and its synonyms
    """
    keywords: set[str] = process(Config.SECURITY_RULES_PATH + filename, False)  # no lemma

    word_list: list[str] = []
    for keyword in keywords:
        word_list += list(match_synset(keyword))  # match synonyms

    return set(stemmer(word_list))  # lemma
