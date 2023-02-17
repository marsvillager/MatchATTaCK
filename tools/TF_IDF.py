from nltk import FreqDist
from tools.transform import freq_count


class TfIdf:
    """
    TF-IDF（term frequency–inverse document frequency）: a Digest Algorithm. 评估出一个单词的重要性即信息量
    Tex formula:
        TF(a,w)=\frac{count(a,w)}{count(a,*)}
        - count(a, w)：单词w在攻击手段a中出现的次数
        - count(a, *)：攻击手段a的总词数

        IDF(a)=log\frac{N+1}{N(a)+1} + 1
        - N：语料库中的文档总数
        - N(a)：单词w出现在多少种攻击手段中
    """
    def __init__(self):
        self.words = list[str]
        self.words_all = list[str]

        self.term = FreqDist()
        self.term_num = 0

        self.doc_num = 0
        self.term_all = FreqDist()

    def setter(self, words, doc_num, words_all):
        self.words = words
        self.doc_num = doc_num
        self.words_all = words_all

        self.term = freq_count(self.words)
        self.term_num = len(self.words)
        self.term_all = freq_count(self.words_all)
