import math
import pandas as pd

from tools.clean_data import tokenize
from tools.TF_IDF import TfIdf


def get_id_list(keywords: set[str], mitre_list: pd.DataFrame) -> list[str]:
    """
    Match keywords with mitre attack data and return a list of match result.

    :param keywords: keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return: list of mitre att&ck id
    """
    result_list: list[str] = []
    for keyword in keywords:
        for i in range(mitre_list.shape[0]):
            words: list[str] = (str(mitre_list.loc[i, "name"]) + str(mitre_list.loc[i, "description"]) +
                                str(mitre_list.loc[i, "detects"])).split(' ')
            for word in words:
                if word == keyword:
                    result_list.append(mitre_list.loc[i]["id"])
                    break

    return result_list


def result(keywords: set[str], mitre_list: pd.DataFrame) -> list[tuple]:
    """
    Rank depends on result list.

    :param keywords: keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return: sort result of mitre att&ck id according to its frequency
    """
    result_list: list[str] = get_id_list(keywords, mitre_list)
    rank_item: set[str] = set(result_list)

    # frequencies
    rank_list: dict = {}
    for item in rank_item:
        rank_list[item]: int = result_list.count(item)

    return sorted(rank_list.items(), key=lambda k: k[1], reverse=True)


def tf_idf(keywords: set[str], mitre_list: pd.DataFrame) -> list[tuple]:
    """
    Calculate entropy of every word depends on tf_idf.

    :param keywords:  keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return: sort result of mitre att&ck id according to its tf_idf
    """
    tf_idf_result: dict = {}

    # all
    words_all: list[str] = []
    for i in range(mitre_list.shape[0]):
        names: list[str] = tokenize(mitre_list.loc[i, "name"])
        for name in names:
            words_all.append(name)

        descriptions: list[str] = tokenize(mitre_list.loc[i, "description"])
        for description in descriptions:
            words_all.append(description)

        detects: list[str] = tokenize(mitre_list.loc[i, "detects"])
        for detect in detects:
            words_all.append(detect)

    # single
    for i in range(mitre_list.shape[0]):
        words: list[str] = tokenize(mitre_list.loc[i, "name"]) + \
                           tokenize(mitre_list.loc[i, "description"]) + \
                           tokenize(mitre_list.loc[i, "detects"])

        mitre_item = TfIdf()
        mitre_item.setter(words, mitre_list.shape[0], words_all)

        weight: float = 0
        for keyword in keywords:
            tf: float = mitre_item.term[keyword]/mitre_item.term_num

            if tf != 0:
                weight += tf * (math.log((mitre_item.doc_num + 1)/(mitre_item.term_all[keyword] + 1)) + 1)

                # 单个输出测试
                # if mitre_list.loc[i, "id"] == 'T1078.003':
                #     print(keyword)
                #     print(mitre_item.term[keyword])
                #     print(tf * (math.log((mitre_item.doc_num + 1) / (mitre_item.term_all[keyword] + 1)) + 1))

        tf_idf_result[mitre_list.loc[i, "id"]] = weight

    return sorted(tf_idf_result.items(), key=lambda k: float(k[1]), reverse=True)
