import glob
import time
import pandas as pd
import sys

from security_rules.process.process_data import process, load_file
from tools.rank import tf_idf, result


def tf_idf_test(filename: str, format_list: pd.DataFrame, lemma: bool) -> None:
    """
    Test single file.

    :param filename: security file
    :param format_list: processed data of mitre att&ck data
    :param lemma: word ==> lemma if True, stay the same if False
    :return: None
    """
    # security rules, lemma if True
    keywords: set[str] = process(filename, lemma)

    # match
    # print(result(keywords, format_list))
    print(tf_idf(keywords, format_list))


def tf_idf_test_all(filedir: str, format_list: pd.DataFrame, rank: int, lemma: bool) -> None:
    """
    Test all files.

    :param filedir: directory of security file
    :param format_list: processed data of mitre att&ck data
    :param rank: baseline
    :param lemma: word ==> lemma if True, stay the same if False
    :return: None
    """
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
        # rank_list: list[tuple] = [tag[0] for tag in result(keywords, format_list)[0: rank]]
        tf_idf_rank: list[tuple] = tf_idf(keywords, format_list)
        rank_list: list[tuple] = [tag[0] for tag in tf_idf_rank[0: rank]]
        print("top " + str(rank) + " of match results: " + ", ".join(rank_list))
        print([tag[1][1] for tag in tf_idf_rank[0: rank]])

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
