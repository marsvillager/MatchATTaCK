"""
    Three different strategies have been proposed:
        -(a) key2key and rank
        -(b) rank based on dictionary of synonyms
        -(c) NLP
"""
import os
import pandas as pd


class StopWordError(Exception):
    pass


def get_stop_words(path: str) -> list[str]:
    """
    :param path: relative path of stop words file
    :return: list of stop words
    """
    language_filename = os.path.join(path)
    try:
        with open(language_filename, 'rb') as language_file:
            stop_words = [line.decode('utf-8').strip()
                          for line in language_file.readlines()]
    except IOError:
        raise StopWordError(
            '{0}" file is unreadable, check your installation.'.format(
                language_filename
            )
        )

    return stop_words


def filter_stop_words(words: list, filter_words: list) -> list:
    """
    function: filter stop words and special characters(").")
    notes: case insensitive
    :param words: origin data
    :param filter_words: list of stop words
    :return: data without stop words
    """
    res: list = []
    for word in words:
        flag: bool = True
        for filer_word in filter_words:
            # case insensitive
            if word.upper() == filer_word.upper():
                flag = False
                break
        if flag:
            if ")" in word:  # special case: "timeframe)."
                res.append(word[:-2])
            else:
                res.append(word)
    return res


def deplicate_removal(origin_list: list) -> list:
    """
    function: Remove duplicate data
    :param origin_list: origin data
    :return: results without duplicate data
    """
    res: list = []
    for i in origin_list:
        if i not in res and i.title() not in res:  # case insensitive
            res.append(i)
    return res


def rank(match_list: list) -> list:
    """
    function: sort by frequencies of attack id
    :param: list of attack id
    :return: order the frequencies of attack id from highest to lowest
    """
    # contestants
    filter_list: set = set(match_list)

    # frequencies
    rank_list: dict = {}
    for item in filter_list:
        rank_list[item]: int = match_list.count(item)

    return sorted(rank_list.items(), key=lambda res: res[1], reverse=True)


def attack_key2key(attack_list: pd.DataFrame, key: dict, security_rules_list: list, stop_words_list: list) -> list:
    """
    function: strategy(a) match depends on keywords
    :param attack_list: techniques(attack-pattern) data
    :param key: keywords
    :param security_rules_list: range of keywords
    :param stop_words_list: list of stop words
    :return: lis of attack id
    """
    keywords: list = []
    for security_rules in security_rules_list:
        keywords += key[security_rules].split(' ')

    # filter stop words
    keywords: list = filter_stop_words(keywords, stop_words_list)
    keywords: list = deplicate_removal(keywords)
    print(keywords)

    results: list = []
    for keyword in keywords:
        name_index: pd.DataFrame = attack_list.loc[attack_list['attack_name'].str.contains(keyword, case=False)]
        description_index: pd.DataFrame = \
            attack_list.loc[attack_list['attack_description'].str.contains(keyword, case=False)]

        result: list = []
        for res in name_index.attack_id:
            for tmp in res:
                result.append(tmp)
        for res in description_index.attack_id:
            for tmp in res:
                result.append(tmp)
        # each keyword corresponds to list of attack ids which is not repeated
        for item in tuple(set(result)):
            results.append(item)

    return results


def mitigation_key2key(mitigation_list: pd.DataFrame, key: dict, security_rules_list: list,
                       stop_words_list: list) -> list:
    """
    function: strategy(a) match depends on keywords
    :param mitigation_list: mitigations, correlative techniques and relationships between them
    :param key: keywords
    :param security_rules_list: range of keywords
    :param stop_words_list: list of stop words
    :return: lis of attack id
    """
    keywords: list = []
    for security_rules in security_rules_list:
        keywords += key[security_rules].split(' ')

    # filter stop words
    keywords: list = filter_stop_words(keywords, stop_words_list)
    keywords: list = deplicate_removal(keywords)
    print(keywords)

    results: list = []
    for keyword in keywords:
        result: list = match_filed_name(mitigation_list, keyword, "relationship") + \
                       match_filed_name(mitigation_list, keyword, "mitigation_name") + \
                       match_filed_name(mitigation_list, keyword, "mitigation_description")
        # each keyword corresponds to list of attack ids which is not repeated
        for item in tuple(set(result)):
            results.append(item)

    return results


def match_filed_name(mitigation_list: pd.DataFrame, keyword: str, name: str) -> list:
    """
    function: match depends on filed name of mitigation_list
    :param mitigation_list: list of mitigation mapping technique
    :param keyword: each keyword of security rules
    :param name: filed name
    :return: results of matching
    """
    relationship_index: pd.DataFrame = mitigation_list.loc[
        mitigation_list[name].str.contains(keyword, case=False, na=False)]

    result: list = []
    for res in relationship_index.attack_id:
        result.append(res)

    return result
