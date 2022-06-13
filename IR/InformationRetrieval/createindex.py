import json
import os
from IR.InformationRetrieval.tokens import *
from itertools import chain
from pypinyin import pinyin, Style


def getFlashBackTable(content, index, doc_id):
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
    return index


def createIndex():
    index = {}
    index_title = {}
    files = os.listdir('data/')
    for file in files:
        doc_id = files.index(file)  # 获取文件的索引号
        content = getToken(file)  # 获取json文件内容
        title = getToken(file, title=1)  # 获取json文件标题
        index = getFlashBackTable(content, index, doc_id)
        index_title = getFlashBackTable(title, index_title, doc_id)

    # 索引表排序
    index_sorted = sortDict(index)
    index_title_sorted = sortDict(index_title)
    # 创建词项列表
    word_list = createWordList(index_sorted)
    word_list_title = createWordList(index_title_sorted)

    # 将数据写入文件中
    writeToFile(index, 'json/index.json')
    writeToFile(word_list, 'json/wordlist.json')
    writeToFile(index_title, 'json/index_title.json')
    writeToFile(word_list_title, 'json/wordlist_title.json')


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


def createWordList(inverted_index):
    word_list = []
    for word in inverted_index.keys():
        word_list.append(word)
    return word_list


def writeToFile(data, filename):
    with open(filename, 'w', encoding='UTF-8') as write_f:
        json.dump(data, write_f, indent=4, ensure_ascii=False)


# 获取倒叙索引表
def getIndex(filename):
    with open(f'{filename}', 'r', encoding='UTF-8') as index:
        index = json.load(index)
    return index


# 获取词项列表
def getWordList(filename):
    with open(f'{filename}', 'r', encoding='UTF-8') as word_list:
        word_list = json.load(word_list)
    return word_list
