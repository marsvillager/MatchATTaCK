import multiprocessing
import gensim
import pandas as pd

from random import shuffle
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tools.config import Config


def build_document() -> list:
    """
    Build corpus for training doc2vec model in the format of TaggedDocument.

    :return: TaggedDocument
    """
    docs: list = []

    # Mitre ATT&CK
    mitre_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(full).csv")
    for row_id, row in zip(mitre_list['id'],
                           mitre_list['name'] + ' ' + mitre_list['description'] + ' ' + mitre_list['detects']):
        words = gensim.utils.to_unicode(str(row)).split()
        tags = [row_id]
        docs.append(TaggedDocument(words, tags))

    return docs


def train_model(docs: list) -> list[gensim.models.doc2vec.Doc2Vec]:
    """
    Train two kinds of doc2vec model: PV-DBOW and PV-DM.

    :param docs: corpus used to train
    :return: list[doc2vec model]
    """
    cores = multiprocessing.cpu_count()
    simple_models: list[gensim.models.doc2vec.Doc2Vec] = [
        # PV-DBOW plain
        Doc2Vec(dm=0, vector_size=100, negative=5, hs=0, min_count=10, sample=0, epochs=20, workers=cores),

        # PV-DM w/ default averaging; a higher starting alpha may improve CBOW/PV-DM modes
        Doc2Vec(dm=1, vector_size=100, window=10, negative=5, hs=0, min_count=10, sample=0, epochs=20, workers=cores,
                alpha=0.05, comment='alpha=0.05'),

        # PV-DM w/ concatenation - big, slow, experimental mode
        # window=5 (both sides) approximates paper's apparent 10-word total window size
        Doc2Vec(dm=1, dm_concat=1, vector_size=100, window=5, negative=5, hs=0, min_count=10, sample=0, epochs=20,
                workers=cores),
    ]

    doc_list = docs[:]
    shuffle(doc_list)

    for model in simple_models:
        model.build_vocab(docs)
        print("%s vocabulary scanned & state initialized" % model)

    for model in simple_models:
        print("Training %s" % model)
        model.train(doc_list, total_examples=len(doc_list), epochs=model.epochs)

    return simple_models


def find_similar_words(all_models: list[gensim.models.doc2vec.Doc2Vec], word: str, topn: int) -> None:
    """
    Use model to find similar words, although in the method of Doc2Vec, actually call wv.most_similar, which is the
    abbreviation of word2vec.

    :param all_models: trained doc2vec models
    :param word: target word
    :param topn: number of displays
    :return: None
    """
    result: dict = dict()
    for model in all_models:
        result[str(model)] = model.wv.most_similar(word, topn=topn)

    pd.set_option('expand_frame_repr', False)
    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', 1000)
    # show all rows
    pd.set_option('display.max_rows', None)

    print("TOP " + str(topn) + " of most similar words for '" + word + "'")
    print(pd.DataFrame(result))


def cal_cos(a_vect, b_vect) -> float:
    """
    Calculate the cosine similarity between two vectors.

    :param a_vect: vector a
    :param b_vect: vector b
    :return: cosine similarity
    """
    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0

    for a, b in zip(a_vect, b_vect):
        dot_val += a * b
        a_norm += a ** 2
        b_norm += b ** 2

    if a_norm == 0.0 or b_norm == 0.0:
        cos = -1
    else:
        cos = dot_val / ((a_norm * b_norm) ** 0.5)

    return cos


def rank_by_vector(model: gensim.models.doc2vec.Doc2Vec, docs: list, security_rule: list) -> list:
    """
    Rank depends on the cosine similarity between target doc (security rule) and corpus (mitre att&ck).

    :param model: trained doc2vec models
    :param docs: corpus established previously
    :param security_rule: target doc
    :return: rank results
    """
    inferred_vector = model.infer_vector(security_rule)

    vect_list: dict = {}
    for i, doc in enumerate(docs):
        vector = model.infer_vector(doc_words=docs[i][0])
        vect_list[docs[i][1][0]] = cal_cos(inferred_vector, vector)

    return sorted(vect_list.items(), key=lambda k: k[1], reverse=True)


def find_closest_documents(all_models: list[gensim.models.doc2vec.Doc2Vec], docs: list, security_rule: list, topn: int)\
        -> dict:
    """
    Find the documents that has the closest meaning to the target documents.

    :param all_models: trained doc2vec models
    :param docs: corpus established previously
    :param security_rule: target doc
    :param topn: number of displays
    :return: results of different models
    """
    result: dict = dict()

    # PV-DBOW plain
    result[str(all_models[0])] = rank_by_vector(all_models[0], docs, security_rule)[:topn]

    # PV-DM w/ default averaging; a higher starting alpha may improve CBOW/PV-DM modes
    result[str(all_models[1])] = rank_by_vector(all_models[1], docs, security_rule)[:topn]

    # PV-DM w/ concatenation - big, slow, experimental mode
    result[str(all_models[2])] = rank_by_vector(all_models[2], docs, security_rule)[:topn]

    return result


def show_closest_documents(all_models: list[gensim.models.doc2vec.Doc2Vec], docs: list, security_rule: list, topn: int)\
        -> None:
    """
    Show the documents that has the closest meaning to the target documents.

    :param all_models: trained doc2vec models
    :param docs: corpus established previously
    :param security_rule: target doc
    :param topn: number of displays
    :return: None
    """
    pd.set_option('expand_frame_repr', False)
    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', 1000)
    # show all rows
    pd.set_option('display.max_rows', None)

    print("TOP " + str(topn) + " of closest documents:")
    print(pd.DataFrame(find_closest_documents(all_models, docs, security_rule, topn)))
