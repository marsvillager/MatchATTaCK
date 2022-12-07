from nltk import word_tokenize
from nltk.corpus import stopwords
from tools.config import Config


def tokenize(words: str) -> list[str]:
    """
    Tokenize words.

    :param words: raw text
    :return: tokenized text
    """
    return word_tokenize(words.lower())


def rm_punctuation(words: list[str]) -> list[str]:
    """
    Remove specified punctuations and '//website'.

    :param words: tokenized text
    :return: text without specified punctuations and '//website'
    """
    return [word for word in words if word not in Config.FILTER_PUNCTUATIONS and "//" not in word]


def rm_stop_words(words: list[str]) -> list[str]:
    """
    Remove specified stop words.

    :param words:
    :return: text without stop words
    """
    stop_words: set = set(stopwords.words("english"))
    for word in Config.EXTEND_STOP_WORD:
        stop_words.add(word)

    return [word for word in words if word not in stop_words]
