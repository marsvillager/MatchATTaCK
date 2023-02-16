import nltk
import pandas as pd

from mitre_attack.process.package import format_data
from mitre_attack.process.prepare import update
from security_rules.process.extend import get_synset
from security_rules.process.process_data import process
from tools.config import Config
from tools.rank import result, tf_idf

if __name__ == '__main__':
    print("Download/Update data or not? Please input yes or no:")
    if input() == 'yes':
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

        # mitre att&ck
        update()
        format_list: pd.DataFrame = format_data(False)  # lemma if True
        format_list.to_csv(Config.OUTPUT_CSV + "mitre_data.csv", sep=',', index=False, header=True)

    # security rules, lemma if True
    # keywords: set[str] = process(Config.SECURITY_RULES_PATH + "15022_LoginLogoutAtUnusualTime.yml", False)
    keywords: set[str] = process(Config.SECURITY_RULES_PATH + "00927_Account_Disabled_on_Windows.yml", False)
    print(keywords)
    # keywords: set[str] = get_synset(Config.SECURITY_RULES_PATH + "15022_LoginLogoutAtUnusualTime.yml", True)

    # mitre att&ck
    format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(完整).csv")

    # match
    # print(result(keywords, format_list))
    print(tf_idf(keywords, format_list))
