from data.security_rules.process_data import process
from tools.config import Config


def get_keyword(filename: str) -> set[str]:
    """
    Word representation depends on keywords.

    :param filename: security files
    :return: set(lemma) of keywords
    """
    return process(Config.SECURITY_RULES_PATH + filename, True)
