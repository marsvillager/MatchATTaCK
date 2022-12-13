import os
import subprocess
import stix2 as stix2

from stix2 import FileSystemSource
from tools.config import Config


def update() -> None:
    """
    Download or update mitre attack source data.

    """
    if os.path.exists(Config.MITRE_ATTACK_DATA_PATH + "enterprise-attack"):
        subprocess.call(["git", "-C", Config.MITRE_ATTACK_DATA_PATH, "pull"], shell=False)
    else:
        subprocess.call(["git", "clone", Config.URL, Config.MITRE_ATTACK_DATA_PATH], shell=False)


def get_src(scene: str, filter_list: list[stix2.Filter]) -> list[dict]:
    """
    Extract data depends on stix2.

    :param scene: enterprise-attack, ics-attack, mobile-attack
    :param filter_list: attack-pattern(technique), course-of-action(mitigation)
    :return:
    """
    src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH + scene)

    return src.query(filter_list)
