import nltk
import pandas as pd
import ssl

from mitre_attack.process.package import format_data
from mitre_attack.process.prepare import update
from tools.config import Config
from tools.evaluation import test_all, test

if __name__ == '__main__':
    print("Download/Update data or not? Please input yes or no:")
    if input() == 'yes':
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

        # mitre att&ck
        update()
        # format_list: pd.DataFrame = format_data(False)  # lemma if True
        # format_list.to_csv(Config.OUTPUT_CSV + "mitre_data(full).csv", sep=',', index=False, header=True)

    # mitre att&ck
    # format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(full).csv")
    # format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(LancasterStemmer).csv")
    format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(PorterStemmer).csv")
    # format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(SnowballStemmer).csv")

    # test(Config.SECURITY_RULES_PATH + "/sample/" + "15022_LoginLogoutAtUnusualTime.yml", format_list, True)
    # test_all(Config.SECURITY_RULES_PATH + "/osa_rules_experimental/", format_list, 10, True)
    test_all(Config.SECURITY_RULES_PATH + "/osa_rules/", format_list, 10, True)
    # test_all(Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/", format_list, 10, True)
    # test_all(Config.SECURITY_RULES_PATH + "/fy23_deliverable/rules/", format_list, 10, True)
