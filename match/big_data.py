import os
import gensim
import numpy as np
import pandas as pd

from typing import IO
from data.mitre_attack.process.process_data import output_text, restore_from_csv
from tools.clean_data import tokenize
from tools.config import Config


def word2vec(update_flag: bool) -> None:
    """
    Construct word vector based on mitre att&ck.

    :param update_flag: update
    :return: None
    """
    if update_flag:
        output_text()  # lemma

    train_list: list[str] = os.listdir(Config.OUTPUT_TRANSFORM_TXT)
    train_data: list[list[str]] = []
    for train in train_list:
        train_file: IO = open(Config.OUTPUT_TRANSFORM_TXT + train, "r", encoding="utf-8")
        lines: list[str] = train_file.readlines()
        for line in lines:
            train_data.append(tokenize(line))

    model = gensim.models.Word2Vec(sentences=train_data, min_count=1, vector_size=Config.VECTOR_SIZE)
    model.save(Config.OUTPUT_WORD2VEC_MODULE)


def avg_of_word2vec(model, words_list: set[str]) -> np.ndarray:
    """
    Calculate the average of the sum of word vector in list[str].

    :param model: model of word2vec
    :param words_list: target
    :return: average of the sum of word vector
    """
    tmp_vec: np.ndarray = np.zeros(shape=(1, Config.VECTOR_SIZE))
    num: int = 0
    for word in words_list:
        if word in model.wv.key_to_index.keys():
            num += 1
            tmp_vec: np.ndarray = tmp_vec + model.wv[word]

    return tmp_vec / np.full(shape=(1, Config.VECTOR_SIZE), fill_value=num)


def avg_mitre_word2vec(model) -> dict[str, np.ndarray]:
    """
    Calculate the average of the sum of word vector in each mitre att&ck
    :param model: model of word2vec
    :return: dict{mitre att&ck id, average vector}
    """
    average_dict: dict[str, np.ndarray] = {}
    csv_list: list[str] = os.listdir(Config.OUTPUT_CLASSIFICATION_CSV)
    for csv in csv_list:
        format_list: pd.DataFrame = restore_from_csv(csv)

        for i in range(format_list.shape[0]):
            mitre_words: list[str] = tokenize(format_list.loc[i, "name"] + " " + format_list.loc[i, "description"])

            average_dict.update({format_list.loc[i, "id"]: avg_of_word2vec(model, set(mitre_words))})

    return average_dict
