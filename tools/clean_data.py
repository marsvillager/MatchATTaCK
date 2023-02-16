from nltk import WordPunctTokenizer, word_tokenize
from nltk.corpus import stopwords
from tools.config import Config


def tokenize(words: str) -> list[str]:
    """
    Tokenize words.(two kinds)

    :param words: raw text
    :return: tokenized text
    """
    word_tokenizer = WordPunctTokenizer()

    return word_tokenize(' '.join(word_tokenizer.tokenize(str(words).lower())))


def rm_punctuation(words: list[str]) -> list[str]:
    """
    Remove specified punctuations and '//website'.

    :param words: tokenized text
    :return: text without specified punctuations and '//website'
    """
    return [word for word in words if word not in Config.FILTER_PUNCTUATIONS]


def rm_stop_words(words: list[str]) -> list[str]:
    """
    Remove specified stop words.

    :param words: tokenized text
    :return: text without stop words
    """
    stop_words: set = set(stopwords.words("english"))
    for word in Config.EXTEND_STOP_WORD:
        stop_words.add(word)

    return [word for word in words if word not in stop_words]


def rm_single_word(words: list[str]) -> list[str]:
    """
    Remove single words.

    :param words: tokenized text
    :return: text without single word
    """
    return [word for word in words if len(word) > 1]
