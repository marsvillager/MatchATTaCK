from nltk import pos_tag, WordNetLemmatizer, PorterStemmer, FreqDist, LancasterStemmer, SnowballStemmer

from tools.clean_data import tokenize, rm_punctuation, rm_stop_words


def word_pos_tag(words: list[str]) -> list[str]:
    """
    词性标注.

    :param words: list[str]
    :return: list[(word, pos)]
    """
    return pos_tag(words)


def lemmatize(words: list[str]) -> list[str]:
    """
    词性还原.

    :param words: list[str]
    :return: lemmatize the word in the form of n. or v.
    """
    cut_words1: list[str] = []
    for word in words:
        cut_words1.append(WordNetLemmatizer().lemmatize(word, pos='n'))  # 指定还原词性为名词

    cut_words2: list[str] = []
    for cut_word in cut_words1:
        cut_words2.append(WordNetLemmatizer().lemmatize(cut_word, pos='v'))  # 指定还原词性为动词
    return cut_words2


def stemmer(words: list[str]) -> list[str]:
    """
    词干提取.

    :param words: list[str]
    :return: stemmer of the word
    """
    cut_word: list[str] = []
    for word in words:
        # 基于 Porter词干提取算法
        # cut_word.append((PorterStemmer().stem(word)))
        # 基于 Lancaster 词干提取算法
        cut_word.append(LancasterStemmer().stem(word))
        # 基于 Snowball 词干提取算法
        # cut_word.append(SnowballStemmer('english').stem(word))
    return cut_word


def is_lemma(words: str, lemma: bool):
    if lemma:
        return set(stemmer(lemmatize(rm_stop_words(rm_punctuation(tokenize(words))))))
    else:
        return set(lemmatize(rm_stop_words(rm_punctuation(tokenize(words)))))
