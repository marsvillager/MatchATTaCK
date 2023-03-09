import gc
import json
import numpy as np
import os
import re
import string
import torch

from pytorch_transformers import *
from sklearn.cluster import KMeans
from tools.config import Config

kmeans = KMeans(n_clusters=6, random_state=0, init='k-means++', n_init=10, max_iter=10)
device = torch.device('cpu')


def load_model():
    os.chdir(Config.BASE_DIR)
    print(os.getcwd())
    # 保存模型的时候保存了相对目录，要是在其它目录下调用，就会出现 ModuleNotFoundError: No module named 'model_en' 的问题
    model_en = torch.load('./WantWords/website_RD/models/En.model', map_location=lambda storage, loc: storage)
    return model_en


def process_data():
    wd_data_en_ = json.load(open(Config.PROMPT_RESOURCE_PATH + 'wd_def_for_website_En.json'))

    wd_data_en = wd_data_en_.copy()
    wd_defi_en = wd_data_en_.copy()
    for wd in wd_data_en_:
        wd_data_en[wd] = {'w': wd_data_en_[wd]['word'], 'P': wd_data_en_[wd]['POS']}
        wd_defi_en[wd] = wd_data_en_[wd]['definition']
    del wd_data_en_
    gc.collect()

    return wd_data_en, wd_defi_en


def word2feature(dataset, word_num, feature_num, feature_name):  # extracting features of each word in the sentence.
    max_feature_num = max([len(instance[feature_name]) for instance in dataset])
    ret = np.zeros((word_num, max_feature_num), dtype=np.int64)
    ret.fill(feature_num)
    for instance in dataset:
        if ret[instance['word'], 0] != feature_num:
            # this target_words has been given a feature mapping, because same word with different definition in dataset
            continue
        feature = instance[feature_name]
        ret[instance['word'], :len(feature)] = np.array(feature)
    return torch.tensor(ret, dtype=torch.int64, device=device)


def label_multi_hot(labels, num):
    sm = np.zeros((len(labels), num), dtype=np.float32)
    for i in range(len(labels)):
        for s in labels[i]:
            if s >= num:
                break
            sm[i, s] = 1
    return sm


def mask_no_feature(label_size, wd2fea, feature_num):
    mask_no_fea = torch.zeros(label_size, dtype=torch.float32, device=device)
    for i in range(label_size):
        feas = set(wd2fea[i].tolist()) - set([feature_num])
        if len(feas) == 0:
            mask_no_fea[i] = 1
    return mask_no_fea


def process_multi_channel():
    (_, (_, label_size, _, _), (word2index_en, index2word_en, index2sememe, index2lexname, index2rootaffix)) = np.load(
        Config.PROMPT_RESOURCE_PATH + 'data_inUse1_en.npy', allow_pickle=True)
    (data_train_idx, data_dev_idx, data_test_500_seen_idx, data_test_500_unseen_idx, data_defi_c_idx,
     data_desc_c_idx) = np.load(Config.PROMPT_RESOURCE_PATH + 'data_inUse2_en.npy', allow_pickle=True)
    data_all_idx = data_train_idx + data_dev_idx + data_test_500_seen_idx + data_test_500_unseen_idx + data_defi_c_idx
    index2word_en = np.array(index2word_en)
    print("label_size: " + str(label_size))

    sememe_num = len(index2sememe)
    print("\n" + "sememe_num: " + str(sememe_num))
    wd2sem = word2feature(data_all_idx, label_size, sememe_num, 'sememes')
    print(wd2sem.shape)
    print(wd2sem)
    wd_sems_ = label_multi_hot(wd2sem, sememe_num)
    wd_sems_ = torch.from_numpy(np.array(wd_sems_)).to(device)
    print(wd_sems_.shape)
    print(wd_sems_.nonzero())

    lexname_num = len(index2lexname)
    print("\n" + "lexname_num: " + str(lexname_num))
    wd2lex = word2feature(data_all_idx, label_size, lexname_num, 'lexnames')
    print(wd2lex.shape)
    wd_lex = label_multi_hot(wd2lex, lexname_num)
    wd_lex = torch.from_numpy(np.array(wd_lex)).to(device)
    print(wd_lex.shape)
    print(wd_lex.nonzero())

    rootaffix_num = len(index2rootaffix)
    print("\n" + "rootaffix_num: " + str(rootaffix_num))
    wd2ra = word2feature(data_all_idx, label_size, rootaffix_num, 'root_affix')
    print(wd2ra.shape)
    wd_ra = label_multi_hot(wd2ra, rootaffix_num)
    wd_ra = torch.from_numpy(np.array(wd_ra)).to(device)
    print(wd_ra.shape)
    print(wd_ra.nonzero())

    mask_s_ = mask_no_feature(label_size, wd2sem, sememe_num)
    mask_l = mask_no_feature(label_size, wd2lex, lexname_num)
    mask_r = mask_no_feature(label_size, wd2ra, rootaffix_num)

    del data_all_idx, data_train_idx, data_dev_idx, data_test_500_seen_idx, data_test_500_unseen_idx, data_defi_c_idx
    gc.collect()

    index2synset_en = [[] for i in range(len(word2index_en))]
    for line in open(Config.PROMPT_RESOURCE_PATH + 'word_synsetWords.txt').readlines():
        wd = line.split()[0]
        synset = line.split()[1:]
        for syn in synset:
            index2synset_en[word2index_en[wd]].append(word2index_en[syn])

    return word2index_en, index2word_en, wd_sems_, wd_lex, wd_ra, mask_s_, mask_l, mask_r


def score2hex_str(score, maxsc):
    thr = maxsc / 1.5
    length = len(score)
    ret = ['00'] * length
    for i in range(length):
        res = int(200 * (score[i] - thr) / thr)
        if res > 15:
            ret[i] = hex(res)[2:]
        else:
            break
    return ret


def get_class2class(r, score):
    per_cluster = [[], [], [], [], [], []]
    for i in range(Config.GET_NUM):
        per_cluster[r[i]].append(score[i])
    score_pc = []
    for i in range(6):
        length = len(per_cluster[i]) if len(per_cluster[i]) < 5 else 5
        score_pc.append(sum(per_cluster[i][:length]) / length)
    ind = [indsc[0] for indsc in sorted(enumerate(score_pc), key=lambda x: x[1], reverse=True)]
    class2class = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        class2class[ind[i]] = i
    return class2class


def score(description):
    model_en = load_model()
    mode_en = Config.MODE_en
    wd_data_en, wd_defi_en = process_data()
    words_t = torch.tensor(np.array([0]))
    word2index_en, index2word_en, wd_sems_, wd_lex, wd_ra, mask_s_, mask_l, mask_r = process_multi_channel()

    tokenizer_class = BertTokenizer
    tokenizer_en = tokenizer_class.from_pretrained('bert-base-uncased')

    def_words = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)
    def_words = def_words.lower()
    def_words = def_words.strip().split()
    def_word_idx = []

    if len(def_words) > 0:
        for def_word in def_words:
            if def_word in word2index_en:
                def_word_idx.append(word2index_en[def_word])
            else:
                def_word_idx.append(word2index_en['<OOV>'])

        # [CLS] 标志放在第一个句子的首位，经过 BERT 得到的的表征向量 C 可以用于后续的分类任务
        defi = '[CLS] ' + description
        def_word_idx = tokenizer_en.encode(defi)[:60]
        # [SEP] 标志用于分开两个输入句子，例如输入句子 A 和 B，要在句子 A，B 后面增加 [SEP] 标志
        def_word_idx.extend(tokenizer_en.encode('[SEP]'))
        definition_words_t = torch.tensor(np.array(def_word_idx), dtype=torch.int64, device=device)
        definition_words_t = definition_words_t.unsqueeze(0)  # batch_size = 1

        score = model_en('test', x=definition_words_t, w=words_t, ws=wd_sems_, wl=wd_lex, wr=wd_ra, msk_s=mask_s_,
                         msk_l=mask_l, msk_r=mask_r, mode=mode_en)
        sc, indices = torch.sort(score, descending=True)
        predicted = indices[0, :Config.NUM_RESPONSE].detach().cpu().numpy()
        score = sc[0, :Config.NUM_RESPONSE].detach().numpy()
        maxsc = sc[0, 0].detach().item()
        s2h = score2hex_str(score, maxsc)

        r = kmeans.fit_predict(model_en.embedding.weight.data[predicted[:Config.GET_NUM]].cpu().numpy())  # GET_NUM
        class2class = get_class2class(r, score[:Config.GET_NUM])
    else:
        return "输入为空"

    ret = []
    if len(predicted) > 0:
        res = index2word_en[predicted]
        cn = -1

        def_words = set(def_words)
        for wd in res:
            cn += 1
            if len(wd) > 1 and (wd not in def_words):
                try:
                    ret.append(wd_data_en[wd])  # wd_data_en[wd] = {'word': word, 'definition':defis, 'POS':['n']}]
                    ret[len(ret) - 1]['c'] = s2h[cn]
                    # 必须转为int，否则其实是int64类型，会报不能json序列化的错误
                    ret[len(ret) - 1]['C'] = class2class[int(r[cn])]
                    ret[len(ret) - 1]['d'] = wd_defi_en[wd]
                    ret.sort(key=lambda x: x['C'])
                except:
                    continue

    return ret
