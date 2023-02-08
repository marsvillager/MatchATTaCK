import yaml

from tools.config import Config
from tools.transform import is_lemma


def load_file(filename: str) -> dict:
    """
    Load .yml files.

    :param filename: name of security file
    :return: file contents
    """
    f = open(filename, 'r', encoding='utf-8')
    file: str = f.read()
    key: dict = yaml.safe_load(file)
    return key


def process(filename: str, lemma: bool) -> set[str]:
    """
    Process keywords(the last step judgment: word ==> lemma ?).

    :param filename: name of security file
    :param lemma: word ==> lemma if True, stay the same if False
    :return: processed keywords(if word ==> lemma or not)
    """
    keywords: str = ''

    pairs: dict = load_file(filename)
    items: list[str] = Config.SECURITY_RULES_PROP
    for item in items:
        keywords = keywords + " " + pairs[item]

    return is_lemma(keywords, lemma)
