import math

import gensim
import numpy as np
import pandas as pd

from match.big_data import word2vec, avg_of_word2vec, avg_mitre_word2vec
from tools.TF_IDF import TfIdf
from tools.clean_data import tokenize
from tools.config import Config


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
            words: list[str] = tokenize(mitre_list.loc[i, "name"]) + tokenize(mitre_list.loc[i, "description"])
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


def calc_distance(update_flag: bool, keywords: set[str]) -> list[tuple]:
    """
    Calculate distance of two vector(L2-norm, Euclidean Distance).

    :param update_flag: update data if true
    :param keywords: convert keywords to word vector based on word2vec
    :return: sort result of mitre att&ck id according to calculated distance
    """
    word2vec(update_flag)

    model = gensim.models.Word2Vec.load(Config.OUTPUT_WORD2VEC_MODULE)

    security_rule_list: np.ndarray = avg_of_word2vec(model, keywords)
    mitre_list: dict[str, np.ndarray] = avg_mitre_word2vec(model)

    for mitre_id in mitre_list.keys():
        mitre_list[mitre_id] = np.sqrt(np.sum(np.square(mitre_list[mitre_id] - security_rule_list)))

    return sorted(mitre_list.items(), key=lambda k: float(k[1]), reverse=False)


def tf_idf(keywords: set[str], mitre_list: pd.DataFrame):
    """
    Calculate entropy of every word depends on tf_idf.

    :param keywords:  keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return: sort result of mitre att&ck id according to its tf_idf
    """
    tf_idf_result: dict = {}

    words_all: list[str] = []
    for i in range(mitre_list.shape[0]):
        names: list[str] = tokenize(mitre_list.loc[i, "name"])
        for name in names:
            words_all.append(name)

        descriptions: list[str] = tokenize(mitre_list.loc[i, "description"])
        for description in descriptions:
            words_all.append(description)

    for i in range(mitre_list.shape[0]):
        words: list[str] = tokenize(mitre_list.loc[i, "name"]) + tokenize(mitre_list.loc[i, "description"])

        mitre_item = TfIdf()
        mitre_item.setter(words, mitre_list.shape[0], words_all)

        weight: float = 0
        for keyword in keywords:
            tf: float = mitre_item.term[keyword]/mitre_item.term_num
            if tf != 0:
                weight += tf * (math.log((mitre_item.doc_num + 1)/(mitre_item.term_all[keyword] + 1)) + 1)

                # 单个输出
                if mitre_list.loc[i, "id"] == 'T1078.003':
                    print(keyword)
                    print(tf * (math.log((mitre_item.doc_num + 1)/(mitre_item.term_all[keyword] + 1)) + 1))

        tf_idf_result[mitre_list.loc[i, "id"]] = weight

    return sorted(tf_idf_result.items(), key=lambda k: float(k[1]), reverse=True)


def tf_idf_digest(attack_id, mitre_list: pd.DataFrame):
    words_all: list[str] = []
    words_attack_id: list[str] = []
    for i in range(mitre_list.shape[0]):
        names: list[str] = tokenize(mitre_list.loc[i, "name"])
        for name in names:
            words_all.append(name)
            if mitre_list.loc[i, "id"] == attack_id:
                words_attack_id.append(name)

        descriptions: list[str] = tokenize(mitre_list.loc[i, "description"])
        for description in descriptions:
            words_all.append(description)
            if mitre_list.loc[i, "id"] == attack_id:
                words_attack_id.append(description)

    keywords: set[str] = set(words_attack_id)
    mitre_item = TfIdf()
    mitre_item.setter(keywords, mitre_list.shape[0], words_all)

    words_dict: dict[str, float] = {}
    for keyword in keywords:
        tf: float = mitre_item.term[keyword] / mitre_item.term_num
        if tf != 0:
            words_dict[keyword] = tf * (math.log((mitre_item.doc_num + 1) / (mitre_item.term_all[keyword] + 1)) + 1)

    return sorted(words_dict.items(), key=lambda k: float(k[1]), reverse=True)
