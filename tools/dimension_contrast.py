import pandas as pd
import stix2

from typing import IO
from stix2 import Filter
from data.mitre_attack.process import classification
from data.mitre_attack.process.get_data import get_src
from data.mitre_attack.process.process_data import output_text
from tools.clean_data import tokenize
from tools.config import Config
from tools.transform import freq_count_out, freq_count


def before_dimension_reduction(scene: str):
    """
    Calculate dimension(before reduction) through word frequency count.

    :param scene: enterprise or mobile or ics
    :return: file of word frequency count
    """
    data: list[str] = []

    filter_list: list[stix2.Filter] = [
        Filter("type", "=", "attack-pattern")  # technique
        # Filter("type", "=", "course-of-action")  # mitigation
    ]
    # enterprise or ics or mobile
    mitre_datasets: list[dict] = get_src(Config.SCENE[scene], filter_list)
    format_list: pd.DataFrame = classification.format_technique(mitre_datasets)
    for i in range(format_list.shape[0]):
        name: list[str] = tokenize(format_list.loc[i, "name"])
        description: list[str] = []
        if pd.notnull(format_list.loc[i, "description"]):
            description: list[str] = tokenize(format_list.loc[i, "description"])
        data.extend(name)
        data.extend(description)

    freq_count_out(freq_count(data))


def after_dimension_reduction(scene: str, type: str):
    """
    Calculate dimension(after reduction) through word frequency count.

    :param scene: enterprise or mobile or ics
    :param type: technique or mitigation
    :return: file of word frequency count
    """
    data: list[str] = []

    output_text()  # lemma
    file: IO = open(Config.OUTPUT_TRANSFORM_TXT + scene + "_" + type + "_data.txt", "r", encoding="utf-8")
    lines: list[str] = file.readlines()
    for line in lines:
        tokenize_list: list[str] = tokenize(line)
        for word in tokenize_list:
            data.append(word)

    freq_count_out(freq_count(data))
