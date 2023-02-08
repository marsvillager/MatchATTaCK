import nltk
import pandas as pd

from mitre_attack.process.package import format_data, get_data
from mitre_attack.process.prepare import update
from security_rules.process.extend import get_synset
from security_rules.process.process_data import process
from tools.config import Config
from tools.rank import result

if __name__ == '__main__':
    print("Download/Update data or not? Please input yes or no:")
    if input() == 'yes':
        nltk.download('punkt')
        nltk.download('stopwords')

        # mitre att&ck
        update()
        format_list: pd.DataFrame = format_data(True)  # lemma if True
        format_list.to_csv(Config.OUTPUT_CSV + "mitre_data.csv", sep=',', index=False, header=True)

    # security rules, lemma if True
    # keywords: set[str] = process(Config.SECURITY_RULES_PATH + "15022_LoginLogoutAtUnusualTime.yml", True)
    keywords: set[str] = get_synset(Config.SECURITY_RULES_PATH + "15022_LoginLogoutAtUnusualTime.yml", True)

    # mitre att&ck
    format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data.csv")

    # match
    print(result(keywords, format_list))
