from typing import TextIO
from matplotlib import pyplot as plt
from nltk import pos_tag, WordNetLemmatizer, PorterStemmer, FreqDist, LancasterStemmer, SnowballStemmer
from wordcloud import WordCloud
from tools.config import Config


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


def freq_count(words: list[str]) -> FreqDist:
    """
    Count frequency of words.

    :param words: list[str]
    :return: FreqDist.items() --> (word, count_num)
    """
    freq: FreqDist = FreqDist(words)

    return freq


def freq_count_out(freq: FreqDist) -> None:
    """
    Output to .txt file.

    :param freq: FreqDist.items() --> (word, count_num)
    :return: None
    """
    word_freq_file: TextIO = open(Config.OUTPUT_WORD_FREQ, mode="w", encoding="utf-8")

    for key, val in freq.items():
        word_freq_file.write(str(key) + ": " + str(val) + "\n")

    word_freq_file.close()


def word_cloud(words: list[str]) -> None:
    """
    词云制作（词频统计可视化）.

    :param words: list[str]
    :return: None
    """
    wc = WordCloud(collocations=False, background_color='white', width=1600, height=1200)
    wwc = wc.generate(words)
    wwc.to_file(Config.OUTPUT_WORD_CLOUD_PIC)
    plt.figure(figsize=(20, 20))
    plt.imshow(wwc)
    plt.axis("off")
    plt.show()
