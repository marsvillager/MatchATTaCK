# coding:utf-8
import numpy as np
import pandas as pd
import jieba.analyse
import os


# 获取关键词
def get_file_keywords(dir):
    data_array = []  # 每篇文章关键词的二维数组
    set_word = []  # 所有关键词的集合

    try:
        for home, dirs, files in os.walk(dir):  # 遍历文件夹下的每篇文章
            for filename in files:
                fullname = os.path.join(home, filename)
                f = open(fullname, 'r', encoding='utf-8')
                sentence = f.read()
                words = " ".join(jieba.analyse.extract_tags(sentence=sentence, topK=30, withWeight=False,
                                                            allowPOS=('n')))  # TF-IDF分词
                print(words)
                words = words.split(' ')
                data_array.append(words)
                for word in words:
                    if word not in set_word:
                        set_word.append(word)
        set_word = list(set(set_word))  # 所有关键词的集合
        return data_array, set_word
    except Exception as reason:
        print('出现错误：', reason)

        return data_array, set_word


# 初始化矩阵
def build_matrix(set_word):
    edge = len(set_word) + 1  # 建立矩阵，矩阵的高度和宽度为关键词集合的长度+1
    '''matrix = np.zeros((edge, edge), dtype=str)'''  # 另一种初始化方法
    matrix = [['' for j in range(edge)] for i in range(edge)]  # 初始化矩阵
    matrix[0][1:] = np.array(set_word)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(set_word)  # 赋值矩阵的第一行与第一列
    return matrix


# 计算各个关键词的共现次数
def count_matrix(matrix, formated_data):
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
            # 遍历矩阵第一列，跳过下标为0的元素
            # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if matrix[0][row] == matrix[col][0]:
                # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                matrix[col][row] = str(0)
            else:
                counter = 0  # 初始化计数器
                for ech in formated_data:
                    # 遍历格式化后的原始数据，让取出的行关键词和取出的列关键词进行组合，
                    # 再放到每条原始数据中查询
                    if matrix[0][row] in ech and matrix[col][0] in ech:
                        counter += 1
                    else:
                        continue
                matrix[col][row] = str(counter)
    return matrix


if __name__ == '__main__':
    formated_data, set_word = get_file_keywords(r'D:\ATT-and-CK\OccurrenceMatrix\data')
    print(set_word)
    print(formated_data)
    matrix = build_matrix(set_word)
    matrix = count_matrix(matrix, formated_data)
    data = pd.DataFrame(matrix)
    data.to_csv('data.csv', index=0, columns=None, encoding='utf_8_sig')
