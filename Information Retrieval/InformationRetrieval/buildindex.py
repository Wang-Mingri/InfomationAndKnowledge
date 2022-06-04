import os
import json
from itertools import chain

from InformationRetrieval import tokens

from pypinyin import pinyin, Style


def buildIndex():
    index = {}
    content = []
    path = 'data/'  # 获取文件路径
    files = os.listdir(path)
    for file in files:
        doc_id = files.index(file)  # 获取文件的索引号
        content = tokens.getToken(file)  # 获取json文件中内容

        pos = 0  # 倒排索引表中 文档中位置
        for word in content:
            if word not in index:  # 若该分词不在索引表中，创建新的词典
                doc_list = {doc_id: [pos]}
                index[word] = doc_list
            else:
                if doc_id not in index[word]:  # 若该分词在索引表中，该词对应的文章号不存在，创建新list加入词典
                    index[word][doc_id] = [pos]
                else:  # 否则直接在list后面加入该分词位置即可
                    index[word][doc_id].append(pos)
            pos += 1
    # 索引表排序
    index_sorted = sortDict(index)
    # 创建词项列表
    word_list = buildWordList(index_sorted)

    # 将数据写入文件中
    writeToFile(index, 'index.json')
    writeToFile(word_list, 'wordlist.json')


def to_pinyin(s):
    '''转拼音
    :param s: 字符串或列表
    :type s: str or list
    :return: 拼音字符串
    '''
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))


def sortDict(dict):
    sdict = {k: dict[k] for k in sorted(dict.keys(), key=to_pinyin)}
    for stem in sdict:
        sdict[stem] = {k: sdict[stem][k] for k in sorted(sdict[stem].keys())}
    return sdict


def buildWordList(invertedIndex):
    wordList = []
    for word in invertedIndex.keys():
        wordList.append(word)
    return wordList


def writeToFile(data, filename):
    with open(filename, 'w') as write_f:
        json.dump(data, write_f, indent=4, ensure_ascii=False)


# 获取倒叙索引表
def getIndex():
    with open('index.json', 'r') as index:
        index = json.load(index)
    return index


# 获取词项列表
def getWordList():
    with open('wordlist.json', 'r') as word_list:
        word_list = json.load(word_list)
    return word_list


if __name__ == '__main__':
    buildIndex()