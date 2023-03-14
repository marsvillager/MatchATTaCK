import argparse
import os
import sys
import nltk
import pandas as pd
import ssl

from mitre_attack.process.package import format_data
from mitre_attack.process.prepare import update
from WantWords.english_reverse_dictionary import score
from tools.config import Config
from tools.evaluation import test_all, test


def parse_arguments():
    parser = argparse.ArgumentParser(description="Match Security Rules to Mitre ATT&CK.")
    parser.add_argument('-u', '--update', action='store', default=None, help='Download or Update data source.')
    parser.add_argument('-l', '--lemma', action='store', default=True,
                        help='Extract lemma of words if True, else please choose False.')
    parser.add_argument('-a', '--attack', action='store', default=Config.OUTPUT_CSV + "mitre_data(PorterStemmer).csv",
                        help='Tables that store processed data of Mitre ATT&CK. \n'
                             '-(full) means use complete words instead of extracting lemma of words \n'
                             '-(xxxStemmer) means different tools used to extract lemma of words')
    # note: Corresponding lemma tools used in Security Rules do not supply api
    #       (location: function stemmer in ./tools/transform.py)

    parser.add_argument('-f', '--file', action='store', default=None, help='Match single security rule.')
    # e.g.'Config.SECURITY_RULES_PATH + "/sample/" + "15022_LoginLogoutAtUnusualTime.yml"'
    #     './security_rules/data/sample/15022_LoginLogoutAtUnusualTime.yml'

    parser.add_argument('-t', '--test', action='store', default=None, help='Test all files in directory of input.')
    # e.g.'Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/"'
    #     './security_rules/data/fy22_deliverable/rules/'
    parser.add_argument('-n', '--number', action='store', default=10,
                        help='The number is used as a baseline to determine whether the Security Rule passes the test,'
                             'eg. tags in top 10 will be considered PASS the test.')

    parser.add_argument('-p', '--prompt', action='store', default=None,
                        help='Prompt words to supply more accuracy description.')

    return parser.parse_args()


def check_arguments(args):
    if not os.path.exists(Config.MITRE_ATTACK_DATA_PATH + "enterprise-attack"):
        sys.exit('Error: You must Download or Update date source first, please input argument -u.')

    if args.update:
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

    if not args.lemma:
        format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(full).csv")
    else:
        if not os.path.exists(args.attack):
            sys.exit('Error: processed data of Mitre ATT&CK does not exist.')
        else:
            format_list: pd.DataFrame = pd.read_csv(args.attack)

    if args.file:
        print(args.file)
        if not os.path.exists(args.file):
            sys.exit('Error: Security Rule file does not exist.')
        else:
            test(args.file, format_list, args.lemma)

    if args.test:
        if not os.path.exists(args.test):
            sys.exit('Error: Directory does not exist.')
        else:
            test_all(args.test, format_list, args.number, args.lemma)

    if args.prompt:
        results = score(args.prompt)
        for result in results:
            print(result)


if __name__ == '__main__':
    args = parse_arguments()
    check_arguments(args)
