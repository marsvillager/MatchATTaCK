import pandas as pd

from tools.config import Config


def format_technique(mitre_datasets: list[dict]) -> pd.DataFrame:
    """
    Extract technique data which is key to process then match.

    :param mitre_datasets: raw data
    :return: key data
    """
    format_list: list[dict] = []
    for mitre_data in mitre_datasets:
        if 'description' in mitre_data:
            format_dict: dict[str, str] = {"id": mitre_data["external_references"][0]["external_id"],
                                           "scene": mitre_data["x_mitre_domains"][0],
                                           "type": Config.COMPARISON_TABLE[mitre_data["type"]],
                                           "name": mitre_data["name"],
                                           "description": mitre_data["description"]}
        else:
            format_dict: dict[str, str] = {"id": mitre_data["external_references"][0]["external_id"],
                                           "scene": mitre_data["x_mitre_domains"][0],
                                           "type": Config.COMPARISON_TABLE[mitre_data["type"]],
                                           "name": mitre_data["name"],
                                           "description": ''}

        format_list.append(format_dict)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    return pd.DataFrame(format_list)


def format_mitigation(mitre_datasets: list[dict]) -> pd.DataFrame:
    """
    Extract mitigation data which is key to process then match.

    :param mitre_datasets: raw data
    :return: key data
    """
    format_list: list[dict] = []
    for mitre_data in mitre_datasets:
        format_dict = {"id": mitre_data["external_references"][0]["external_id"],
                       "scene": mitre_data["x_mitre_domains"][0],
                       "type": Config.COMPARISON_TABLE[mitre_data["type"]],
                       "name": mitre_data["name"],
                       "description": mitre_data["description"]}
        format_list.append(format_dict)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    return pd.DataFrame(format_list)


def output_format(format_list: pd.DataFrame) -> None:
    """
    Output to table.

    :param format_list: data in the form of pd.DataFrame
    :return: None
    """
    scene: str = str(format_list.loc[0, "scene"]).split("-")[0]
    type: str = str(format_list.loc[0, "type"])
    format_list.to_csv(Config.OUTPUT_CLASSIFICATION_CSV + scene + "_" + type + "_data.csv", sep=',', index=False,
                       header=True)
