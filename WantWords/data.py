import json
import os
import numpy as np
import torch.utils.data

data_path = os.path.join('.', 'data')
device = torch.device('cpu')


def data2index(data_x, word2index, sememe2index, lexname2index, rootaffix2index, rootaffix_freq, frequency):
    data_x_idx = list()
    for instance in data_x:
        sememe_idx = [sememe2index[se] for se in instance['sememes']]
        lexname_idx = [lexname2index[ln] for ln in instance['lexnames']]
        rootaffix_idx = [rootaffix2index[ra] for ra in instance['root_affix'] if rootaffix_freq[ra] >= frequency]
        def_word_idx = list()
        def_words = instance['definitions'].strip().split()
        if len(def_words) > 0:
            for def_word in def_words:
                if def_word in word2index and def_word != instance['word']:
                    def_word_idx.append(word2index[def_word])
                else:
                    def_word_idx.append(word2index['<OOV>'])
            data_x_idx.append({'word': word2index[instance['word']], 'lexnames': lexname_idx,
                               'root_affix': rootaffix_idx, 'sememes': sememe_idx, 'definition_words': def_word_idx})
        else:
            # print(instance['word'], instance['definitions'])  # some is null
            pass
    return data_x_idx


def load_data(frequency):
    print('Loading dataset...')
    data_train = json.load(open(os.path.join(data_path, 'data_train.json')))
    data_dev = json.load(open(os.path.join(data_path, 'data_dev.json')))
    data_test_500_rand1_seen = json.load(open(os.path.join(data_path, 'data_test_500_rand1_seen.json')))
    # data_test_500_others
    data_test_500_rand1_unseen = json.load(open(os.path.join(data_path, 'data_test_500_rand1_unseen.json')))
    data_defi_c = json.load(open(os.path.join(data_path, 'data_defi_c.json')))
    data_desc_c = json.load(open(os.path.join(data_path, 'data_desc_c.json')))
    lines = open(os.path.join(data_path, 'target_words.txt')).readlines()
    target_words = [line.strip() for line in lines]
    label_size = len(target_words)+2
    print('target_words (include <PAD><OOV>): ', label_size)
    lines = open(os.path.join(data_path, 'lexname_all.txt')).readlines()
    lexname_all = [line.strip() for line in lines]
    label_lexname_size = len(lexname_all)
    print('label_lexname_size: ', label_lexname_size)
    lines = open(os.path.join(data_path, 'root_affix_freq.txt')).readlines()
    rootaffix_freq = {}
    for line in lines:
        rootaffix_freq[line.strip().split()[0]] = int(line.strip().split()[1])
    lines = open(os.path.join(data_path, 'rootaffix_all.txt')).readlines()
    rootaffix_all = [line.strip() for line in lines]
    label_rootaffix_size = len(rootaffix_all)
    print('label_rootaffix_size: ', label_rootaffix_size)
    lines = open(os.path.join(data_path, 'sememes_all.txt')).readlines()
    sememes_all = [line.strip() for line in lines]
    label_sememe_size = len(sememes_all)+1
    print('label_sememe_size: ', label_sememe_size)
    vec_inuse = json.load(open(os.path.join(data_path, 'vec_inuse.json')))
    vocab = list(vec_inuse)
    vocab_size = len(vocab)+2
    print('vocab (embeddings in use)(include <PAD><OOV>): ', vocab_size)
    word2index = dict()
    index2word = list()
    word2index['<PAD>'] = 0
    word2index['<OOV>'] = 1
    index2word.extend(['<PAD>', '<OOV>'])
    index2word.extend(vocab)
    word2vec = np.zeros((vocab_size, len(list(vec_inuse.values())[0])), dtype=np.float32)
    for wd in vocab:
        index = len(word2index)
        word2index[wd] = index
        word2vec[index, :] = vec_inuse[wd]
    sememe2index = dict()
    index2sememe = list()
    for sememe in sememes_all:
        sememe2index[sememe] = len(sememe2index)
        index2sememe.append(sememe)
    lexname2index = dict()
    index2lexname = list()
    for ln in lexname_all:
        lexname2index[ln] = len(lexname2index)
        index2lexname.append(ln)
    rootaffix2index = dict()
    index2rootaffix = list()
    for ra in rootaffix_all:
        if rootaffix_freq[ra] >= frequency:
            rootaffix2index[ra] = len(rootaffix2index)
            index2rootaffix.append(ra)
    data_train_idx = data2index(data_train, word2index, sememe2index, lexname2index, rootaffix2index, rootaffix_freq,
                                frequency)
    print('data_train size: %d' % len(data_train_idx))
    data_dev_idx = data2index(data_dev, word2index, sememe2index, lexname2index, rootaffix2index, rootaffix_freq,
                              frequency)
    print('data_dev size: %d' % len(data_dev_idx))
    data_test_500_seen_idx = data2index(data_test_500_rand1_seen, word2index, sememe2index, lexname2index,
                                        rootaffix2index, rootaffix_freq, frequency)
    print('data_test_seen size: %d' % len(data_test_500_seen_idx))
    data_test_500_unseen_idx = data2index(data_test_500_rand1_unseen, word2index, sememe2index, lexname2index,
                                          rootaffix2index, rootaffix_freq, frequency)
    print('data_test_unseen size: %d' % len(data_test_500_unseen_idx))
    data_defi_c_idx = data2index(data_defi_c, word2index, sememe2index, lexname2index, rootaffix2index, rootaffix_freq,
                                 frequency)
    data_desc_c_idx = data2index(data_desc_c, word2index, sememe2index, lexname2index, rootaffix2index, rootaffix_freq,
                                 frequency)
    print('data_desc size: %d' % len(data_desc_c_idx))
    return word2index, index2word, word2vec, (index2sememe, index2lexname, index2rootaffix), \
        (label_size, label_lexname_size, label_rootaffix_size, label_sememe_size), \
        (data_train_idx, data_dev_idx, data_test_500_seen_idx, data_test_500_unseen_idx, data_defi_c_idx,
         data_desc_c_idx)
