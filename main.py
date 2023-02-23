import nltk
import pandas as pd
from nltk import WordNetLemmatizer

from mitre_attack.process.package import format_data
from mitre_attack.process.prepare import update
from tools.config import Config
from tools.evaluation import test_all, test
from tools.transform import lemmatize, stemmer, is_lemma, word_pos_tag

if __name__ == '__main__':
    print("Download/Update data or not? Please input yes or no:")
    if input() == 'yes':
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

        # mitre att&ck
        update()
        # format_list: pd.DataFrame = format_data(False)  # lemma if True
        # format_list.to_csv(Config.OUTPUT_CSV + "mitre_data.csv", sep=',', index=False, header=True)

    # mitre att&ck
    format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(完整).csv")
    # format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(lemma2.0).csv")

    # test(Config.SECURITY_RULES_PATH + "/sample/" + "15022_LoginLogoutAtUnusualTime.yml", format_list)
    # test_all(Config.SECURITY_RULES_PATH + "/osa_rules/", format_list, 10)
    # test_all(Config.SECURITY_RULES_PATH + "/osa_rules_experimental/", format_list, 10)
    test_all(Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/", format_list, 10)
    # test_all(Config.SECURITY_RULES_PATH + "/fy23_deliverable/rules/", format_list, 10)
