from nltk import FreqDist
from tools.transform import freq_count


class TfIdf:
    """
    TF-IDF（term frequency–inverse document frequency）: a Digest Algorithm. 评估出一个单词的重要性即信息量
    Tex formula:
        TF(a_i,w_j)=\frac{count(a_i,w_j)}{limit(count(a_i,*))}
        - count(a_i, w_j)：单词 w_j 在攻击手段 a_i 中出现的次数
        - count(a_i, *)：攻击手段 a_i 的总词数
        - limit：总词数小于某阈值时将强制调节为该阈值

        IDF(a_i)=log\frac{N+1}{N(w_j)+1} + 1
        - N：攻击手段总数
        - N(w_j)：单词 w_j 出现在多少种攻击手段中
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
