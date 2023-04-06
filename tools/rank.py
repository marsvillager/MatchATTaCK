import math
import numpy as np
import pandas as pd

from tools.clean_data import tokenize
from tools.TF_IDF import TfIdf
from tools.config import Config
from tools.page_rank import build_matrix, pagerank


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


def unskilled_result(keywords: set[str], mitre_list: pd.DataFrame) -> list[tuple]:
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


def se_result(keywords: set[str], mitre_list: pd.DataFrame) -> list[tuple]:
    """
    Calculate entropy of every word depends on search_engine.

    :param keywords:  keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :return: sort result of mitre att&ck id according to its search_engine_score
    """
    n: int = mitre_list.shape[0]
    result: dict = {}

    # page rank
    adj_matrix: np.ndarray = build_matrix(mitre_list)
    scores = pagerank(adj_matrix)

    # all
    words_all: list[str] = []
    for i in range(n):
        names: list[str] = tokenize(mitre_list.loc[i, "name"])
        if str(names) != 'nan':
            for name in names:
                words_all.append(name)

        descriptions: list[str] = tokenize(mitre_list.loc[i, "description"])
        if str(descriptions) != 'nan':
            for description in descriptions:
                words_all.append(description)

        detects: list[str] = tokenize(mitre_list.loc[i, "detects"])
        if str(detects) != 'nan':
            for detect in detects:
                words_all.append(detect)

    # single
    for i in range(n):
        words: list[str] = [word for word in tokenize(mitre_list.loc[i, "name"]) if word != 'nan'] + \
                           [word for word in tokenize(mitre_list.loc[i, "description"]) if word != 'nan'] + \
                           [word for word in tokenize(mitre_list.loc[i, "detects"]) if word != 'nan']

        mitre_item = TfIdf()
        mitre_item.setter(words, n, words_all)

        # fix: the total number of mitre_item, that is term_num is too small
        if len(words) < Config.ADJUST_TF:
            mitre_item.term_num = Config.ADJUST_TF

        weight: float = 0
        pass_words: list[str] = []
        # print(mitre_list.loc[i, "id"])
        for keyword in keywords:
            tf: float = mitre_item.term[keyword]/mitre_item.term_num

            if tf != 0:
                pass_words.append(keyword)
                idf: float = math.log((mitre_item.doc_num + 1)/(mitre_item.term_all[keyword] + 1)) + 1
                # print("keyword: " + keyword +
                #       " word: " + str(mitre_item.term[keyword]) + " words: " + str(mitre_item.term_num) +
                #       " docs: " + str(mitre_item.doc_num) + " doc: " + str(mitre_item.term_all[keyword] + 1) +
                #       " tf: " + str(tf) + "  idf: " + str(idf))
                weight += tf * idf

        page_rank_score = n/10 * scores[i]  # multiply n/10 to balance tf-idf and page-rank
        # if page_rank_score > 1:
        #     page_rank_score = 1  # limit page rank score

        # print(Config.SCORE * weight)
        # print((1 - Config.SCORE) * n * scores[i])

        result[mitre_list.loc[i, "id"]] = [Config.SCORE * weight + (1 - Config.SCORE) * page_rank_score, pass_words]

    return sorted(result.items(), key=lambda k: float(k[1][0]), reverse=True)


def show_result(keywords: set[str], mitre_list: pd.DataFrame, topn: int) -> None:
    """
    Show rank list depends on search_engine.

    :param keywords:  keywords of security rules
    :param mitre_list: processed data of mitre att&ck data
    :param topn: only show the first few
    :return: sort result of mitre att&ck id according to its search_engine_score
    """
    pd.set_option('expand_frame_repr', False)
    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', 1000)
    # show all rows
    pd.set_option('display.max_rows', None)

    tmp: list[tuple] = se_result(keywords, mitre_list)[:topn]
    se_dict: dict = dict()
    se_dict['id'] = [x[0] for x in tmp]
    se_dict['weight'] = [x[1][0] for x in tmp]
    se_dict['words'] = [x[1][1] for x in tmp]
    print("TOP " + str(topn) + " of closest documents:")
    print(pd.DataFrame(se_dict))
