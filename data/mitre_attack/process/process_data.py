import os
import pandas as pd

from tools.clean_data import tokenize, rm_punctuation, rm_stop_words
from tools.transform import lemmatize, stemmer
from tools.config import Config
from typing import IO


def restore_from_csv(csv_name: str) -> pd.DataFrame:
    """
    Restore formatted data from .csv file(output first).
    Because linking mitigations to techniques(depends on relationship) is time-consuming.

    :return: restored data in the form of pd.DataFrame
    """
    format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CLASSIFICATION_CSV + csv_name)

    for i in range(format_list.shape[0]):
        name: list[str] = stemmer(lemmatize(rm_stop_words(rm_punctuation(tokenize(format_list.loc[i, "name"])))))
        if pd.notnull(format_list.loc[i, "description"]):
            description: list[str] = stemmer(
                lemmatize(rm_stop_words(rm_punctuation(tokenize(format_list.loc[i, "description"])))))
        format_list.loc[i, "name"]: str = " ".join(name)
        format_list.loc[i, "description"]: str = " ".join(description)

    return format_list


def output_text() -> None:
    """
    Only output lemma of [name] and [description] for analysing characteristics of words.

    :return: None
    """
    csv_list: list[str] = os.listdir(Config.OUTPUT_CLASSIFICATION_CSV)
    for csv in csv_list:
        format_list: pd.DataFrame = restore_from_csv(csv)

        scene: str = str(format_list.loc[0, "scene"]).split("-")[0]
        type: str = str(format_list.loc[0, "type"])

        format_file: IO = open(Config.OUTPUT_TRANSFORM_TXT + scene + "_" + type + "_data.txt", mode="w",
                               encoding="utf-8")

        for i in range(format_list.shape[0]):
            format_file.write(format_list.loc[i, "name"] + "\n")
            format_file.write(format_list.loc[i, "description"] + "\n")

        format_file.close()
