import gensim
import numpy as np
import pandas as pd

from match.big_data import word2vec, avg_of_word2vec, avg_mitre_word2vec
from tools.config import Config


def get_id_list(keywords: set[str], mitre_list: pd.DataFrame) -> list[str]:
    """
    Match keywords with mitre attack data and return a list of match result.

    :param keywords: keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return:
    """
    result_list: list[str] = []
    for keyword in keywords:
        for i in range(mitre_list.shape[0]):
            if keyword in mitre_list.loc[i]["name"] or keyword in mitre_list.loc[i]["description"]:
                result_list.append(mitre_list.loc[i]["id"])

    return result_list


def result(keywords: set[str], mitre_list: pd.DataFrame) -> list[tuple]:
    """
    Rank depends on result list.

    :param keywords:
    :param mitre_list:
    :return:
    """
    result_list: list[str] = get_id_list(keywords, mitre_list)
    rank_item: set[str] = set(result_list)

    # frequencies
    rank_list: dict = {}
    for item in rank_item:
        rank_list[item]: int = result_list.count(item)

    return sorted(rank_list.items(), key=lambda k: k[1], reverse=True)


def calc_distance(update_flag: bool, keywords: set[str]) -> list[tuple]:
    word2vec(update_flag)

    model = gensim.models.Word2Vec.load(Config.OUTPUT_WORD2VEC_MODULE)

    security_rule_list: np.ndarray = avg_of_word2vec(model, keywords)
    mitre_list: dict[str, np.ndarray] = avg_mitre_word2vec(model)

    for mitre_id in mitre_list.keys():
        mitre_list[mitre_id] = np.sqrt(np.sum(np.square(mitre_list[mitre_id] - security_rule_list)))

    return sorted(mitre_list.items(), key=lambda k: float(k[1]), reverse=True)
