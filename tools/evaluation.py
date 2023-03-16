import glob
import time
import gensim
import pandas as pd
import sys

from security_rules.process.process_data import process, load_file
from tools.doc2vec import build_document, find_closest_documents, train_model
from tools.rank import tf_idf


def test_all(filedir: str, method: str, format_list: pd.DataFrame, model: int, num: int, lemma: bool) -> None:
    """
    Test all files.

    :param filedir: directory of security file
    :param method: tf-idf or doc2vec
    :param num: baseline
    :param lemma: word ==> lemma if True, stay the same if False
    :return: None
    """
    if method != 'tf-idf' and method != 'doc2vec':
        sys.exit('Error: Please confirm the way to evaluate and choose "tf-idf" or "doc2vec".')

    if method == 'doc2vec':
        all_docs: list = build_document()
        models: list[gensim.models.doc2vec.Doc2Vec] = train_model(all_docs)
        if 0 < model <= len(models):
            model_name = str(models[model - 1])
            print("\nUsing doc2vec model: " + model_name + '\n')
        else:
            sys.exit('Error: Please input correct number to select model between ' + str([str(item) for item in models])
                     + '.')

    time_start: float = time.perf_counter()

    id_file: str = filedir + '*.yml'

    all_test: int = len(glob.glob(id_file))
    actual_test: int = 0
    tag_test: int = 0
    pass_count: int = 0

    for file in glob.glob(id_file):
        actual_test += 1
        print(str(actual_test) + "/" + str(all_test))
        print(file)

        pairs: dict = load_file(file)
        # if pairs['tags'] is None or pairs['tags'] == '':
        if 'description' not in pairs or pairs['tags'] is None or pairs['tags'] == '':
            print("未打标\n")
            continue

        print(pairs['tags'])
        tag_list: list = [".".join(tag.split('.')[2:]) for tag in pairs['tags'] if 'attack' in tag and 'T' in tag]
        if len(tag_list) == 0:
            print("未打标\n")
            continue

        print("tags of security rules: " + ", ".join(tag_list))
        tag_test += 1

        # security rules, lemma if True
        keywords: set[str] = process(file, lemma)
        print("keywords: " + ", ".join(keywords))

        # match
        if method == 'tf-idf':
            tf_idf_rank: list[tuple] = tf_idf(keywords, format_list)
            rank_list: list[tuple] = [tag[0] for tag in tf_idf_rank[0: num]]
            print("top " + str(num) + " of match results: " + ", ".join(rank_list))
            print([tag[1][1] for tag in tf_idf_rank[0: num]])
        elif method == 'doc2vec':
            doc2vec_rank: list[str] = find_closest_documents(models, all_docs, list(keywords), num)[model_name]
            rank_list: list[str] = [tag[0] for tag in doc2vec_rank]
            print("top " + str(num) + " of match results: " + ", ".join(rank_list))

        for tag in tag_list:
            if tag in rank_list:
                pass_count += 1
                print("pass")
                break

        print("\n")

    print("all tests: " + str(all_test))
    print("actual tests: " + str(actual_test))
    print("tag tests: " + str(tag_test))
    print("pass: " + str(pass_count))
    if pass_count > 0:
        print("ratio: " + str(pass_count / tag_test))

    time_end: float = time.perf_counter()
    seconds: float = (time_end - time_start)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("run time: " + str(seconds) + "s" + " ≈ %02d:%02d:%02d" % (h, m, s))

    if actual_test == 0:
        sys.exit('Error: Test None.')
