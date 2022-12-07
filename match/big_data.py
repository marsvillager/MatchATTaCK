import os

from data.mitre_attack.process.process_data import output_text, restore_from_csv
from tools.config import Config


def process_data() -> None:
    """
    Output lemma of [name] and [description] to .txt file

    :return: None
    """
    csv_list: list[str] = os.listdir(Config.OUTPUT_CLASSIFICATION_CSV)
    for csv in csv_list:
        output_text(restore_from_csv(csv))
