import argparse
import os
import sys
import gensim
import nltk
import pandas as pd
import ssl

from mitre_attack.process.prepare import update
from tools.doc2vec import build_document, train_model, show_closest_documents
from prompt.english_reverse_dictionary import score
from security_rules.process.process_data import process
from tools.config import Config
from tools.evaluation import test_all
from tools.rank import show_tf_idf


def parse_arguments():
    parser = argparse.ArgumentParser(description="Match Security Rules to Mitre ATT&CK.")
    parser.add_argument('-u', '--update', action='store_true', help='Download or Update data source.')
    parser.add_argument('-l', '--lemma', action='store', default=True,
                        help='Extract lemma of words if True, else please choose False.')
    parser.add_argument('-a', '--attack', action='store', default=Config.OUTPUT_CSV + "mitre_data(PorterStemmer).csv",
                        help='Tables that store processed data of Mitre ATT&CK. \n'
                             '-(full) means use complete words instead of extracting lemma of words \n'
                             '-(xxxStemmer) means different tools used to extract lemma of words')
    # note: Corresponding lemma tools used in Security Rules do not supply api
    #       (location: function stemmer in ./tools/transform.py)

    parser.add_argument('-t', '--tf_idf', action='store', default=None, help='Match single security rule by TF-IDF.')
    # e.g.'Config.SECURITY_RULES_PATH + "/sample/" + "15022_LoginLogoutAtUnusualTime.yml"'
    #     './security_rules/data/sample/15022_LoginLogoutAtUnusualTime.yml'
    parser.add_argument('-tn', '--tf_idf_number', action='store', default=10,
                        help='Show the first few results ranked depends on TF-IDF.')
    parser.add_argument('-tt', '--tf_idf_test', action='store', default=None,
                        help='Test all files in directory of input.')
    # e.g.'Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/"'
    #     './security_rules/data/fy22_deliverable/rules/'
    parser.add_argument('-ttn', '--tf_idf_test_number', action='store', default=10,
                        help='The number is used as a baseline to determine whether the Security Rule passes the test,'
                             'eg. tags in top 10 will be considered PASS the test.')

    parser.add_argument('-d', '--doc2vec', action='store', default=None, help='Match single security rule by Doc2Vec.')
    # e.g.'Config.SECURITY_RULES_PATH + "/sample/" + "15022_LoginLogoutAtUnusualTime.yml"'
    #     './security_rules/data/sample/15022_LoginLogoutAtUnusualTime.yml'
    parser.add_argument('-dn', '--doc2vec_number', action='store', default=10,
                        help='Show the first few results ranked depends on doc2vec.')
    parser.add_argument('-dt', '--doc2vec_test', action='store', default=None,
                        help='Test all files in directory of input.')
    parser.add_argument('-dtm', '--doc2vec_test_model', action='store', default=1,
                        help='Choose one model to test.')
    # e.g.'Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/"'
    #     './security_rules/data/fy22_deliverable/rules/'
    parser.add_argument('-dtn', '--doc2vec_test_number', action='store', default=10,
                        help='The number is used as a baseline to determine whether the Security Rule passes the test,'
                             'eg. tags in top 10 will be considered PASS the test.')

    parser.add_argument('-p', '--prompt', action='store', default=None,
                        help='Prompt words to supply more accuracy description.')

    return parser.parse_args()


def check_arguments(args):
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
        # format_list: pd.DataFrame = format_data(bool(args.lemma))  # lemma if True
        # format_list.to_csv(Config.OUTPUT_CSV + "mitre_data(full).csv", sep=',', index=False, header=True)

    if not os.path.exists(Config.MITRE_ATTACK_DATA_PATH + "enterprise-attack"):
        sys.exit('Error: You must Download or Update date source first, please input argument -u.')

    # the format of transferred argument is string
    if args.lemma == 'False':
        args.lemma: bool = False

    if not args.lemma:
        format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(full).csv")
    else:
        if not os.path.exists(args.attack):
            sys.exit('Error: Processed data of Mitre ATT&CK does not exist.')
        else:
            format_list: pd.DataFrame = pd.read_csv(args.attack)

    if args.tf_idf:
        if not os.path.exists(args.tf_idf):
            sys.exit('Error: Security Rule file does not exist.')
        else:
            keywords: set[str] = process(args.tf_idf, args.lemma)
            show_tf_idf(keywords, format_list, int(args.tf_idf_number))

    if args.tf_idf_test:
        if not os.path.exists(args.tf_idf_test):
            sys.exit('Error: Directory does not exist.')
        else:
            test_all(args.tf_idf_test, 'tf-idf', format_list, 1, int(args.tf_idf_test_number), args.lemma)

    if args.doc2vec:
        if not os.path.exists(args.doc2vec):
            sys.exit('Error: Security Rule file does not exist.')
        else:
            all_docs: list = build_document()
            models: list[gensim.models.doc2vec.Doc2Vec] = train_model(all_docs)
            keywords: set[str] = process(args.doc2vec, False)  # lemma == False
            show_closest_documents(models, all_docs, list(keywords), int(args.doc2vec_number))

    if args.doc2vec_test:
        if not os.path.exists(args.doc2vec_test):
            sys.exit('Error: Directory does not exist.')
        else:
            test_all(args.doc2vec_test, 'doc2vec', format_list, int(args.doc2vec_test_model),
                     int(args.doc2vec_test_number), False)  # lemma == False

    if args.prompt:
        results = score(args.prompt)
        for result in results:
            print(result)


if __name__ == '__main__':
    args = parse_arguments()
    check_arguments(args)
