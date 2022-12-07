import stix2
import pandas as pd

from stix2 import Filter
from data.mitre_attack.process import classification
from data.mitre_attack.process.classification import output_format
from data.mitre_attack.process.get_data import get_src, update
from data.mitre_attack.process.process_data import restore_from_csv
from match.keyword import get_keyword
from match.knowledge import get_synset
from match.rank import result
from tools.config import Config

if __name__ == '__main__':
    """
    1. mitre attack data(lemma)
    """
    print("Download/Update data or not? Please input yes or no:")
    if input() == 'yes':
        # 1.1 Download or update.
        update()

        # 1.2 Classify data.
        filter_list: list[stix2.Filter] = [
            # Filter("type", "=", "attack-pattern")  # technique
            Filter("type", "=", "course-of-action")  # mitigation
        ]
        # enterprise or ics or mobile
        mitre_datasets: list[dict] = get_src(Config.SCENE["enterprise"], filter_list)
        format_list: pd.DataFrame = classification.format_technique(mitre_datasets)
        output_format(format_list)

    mitre_list: pd.DataFrame = restore_from_csv("enterprise" + "_" + "technique" + "_data.csv")

    """
    2. security rules(lemma)
    """
    # 2.1 Word representation depends on keywords.
    # keywords: set[str] = get_keyword("00927_Account_Disabled_on_Windows.yml")
    keywords: set[str] = get_keyword("15022_LoginLogoutAtUnusualTime.yml")

    # 2.2 Word representation depends on knowledge.
    # keywords: set[str] = get_synset("00927_Account_Disabled_on_Windows.yml")
    # keywords: set[str] = get_synset("15022_LoginLogoutAtUnusualTime.yml")

    # 2.3 Word representation depends on big data.

    """
    3. rank
    """
    print(result(keywords, mitre_list))
