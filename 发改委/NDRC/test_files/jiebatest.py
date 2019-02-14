import jieba.analyse
from 国家能源局_first.NEA.mongo import *


def analyzetest(collection):
    content = readcontentstringtest(collection)
    jieba.analyse.set_stop_words('stopwords.dat')
    tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
    for v, n in tags:
        # 权重是小数，为了凑整，乘了一万
        print(v + '\t' + str(int(n * 10000)) + '\n')


def split(collection):
    stopwords = []
    for stopword in open('stopwords.txt', 'r'):
        stopwords.append(stopword.strip())
    content = readcontentstring(collection)
    splitData = jieba.cut(content, cut_all=False, HMM=True)  # 三种模式
    result = ''
    for splitword in splitData:
        if splitword not in stopwords:
            result += splitword + " "
    return result

# analyzetest('最新文件2018-07-08 11:01:15')

