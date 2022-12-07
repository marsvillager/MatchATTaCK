import pandas as pd


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


def result(keywords: set[str], mitre_list: pd.DataFrame):
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

    return sorted(rank_list.items(), key=lambda res: res[1], reverse=True)
