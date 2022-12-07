import _io
import yaml

from tools.clean_data import tokenize, rm_punctuation, rm_stop_words
from tools.config import Config
from tools.transform import lemmatize, stemmer


def load_file(filename: str) -> dict:
    """
    Load .yml files.

    :param filename: name of security file
    :return: file contents
    """
    f: _io.TextIO = open(filename, 'r', encoding='utf-8')
    file: str = f.read()
    key: dict = yaml.safe_load(file)
    return key


def process(filename: str, is_lemma: bool) -> set[str]:
    """
    Process keywords(the last step judgment: word ==> lemma ?).

    :param filename: name of security file
    :param is_lemma: word ==> lemma if True, stay the same if False
    :return: processed keywords(word ==> lemma ?)
    """
    keywords: str = ''

    pairs: dict = load_file(filename)
    items: list[str] = Config.SECURITY_RULES_PROP
    for item in items:
        keywords = keywords + " " + pairs[item]

    if is_lemma:
        return set(stemmer(lemmatize(rm_stop_words(rm_punctuation(tokenize(keywords))))))
    else:
        return set(lemmatize(rm_stop_words(rm_punctuation(tokenize(keywords)))))
