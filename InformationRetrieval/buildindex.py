import os
import json
import tokens

def buildIndex():
    index = {}
    path = '../data/' #获取文件路径
    files = os.listdir(path)
    for file in files:
        doc_id = files.index(file) # 获取文件的索引号
        content = tokens.getToken(file) # 获取json文件中内容

        pos = 0 # 倒排索引表中 文档中位置
        for word in content:
            if word not in index:# 若该分词不在索引表中，创建新的词典
                doc_list = {}
                doc_list[doc_id] = [pos] # 标记文章编号与分词位置
                index[word] = doc_list
            else:
                if doc_id not in index[word]:# 若该分词在索引表中，该词对应的文章号不存在，创建新list加入词典
                    index[word][doc_id] = [pos]
                else:# 否则直接在list后面加入该分词位置即可
                    index[word][doc_id].append(pos)
            pos += 1
    # 索引表排序
    index_sorted = sortDict(index)
    # 创建词项列表
    word_list = buildWordList(index_sorted)

    # 将数据写入文件中
    writeToFile(index, '../index.json')
    writeToFile(word_list, '../wordlist.json')


def sortDict(dict):
    sdict =  { k:dict[k] for k in sorted(dict.keys())}
    for stem in sdict:
        sdict[stem] = { k:sdict[stem][k] for k in sorted(sdict[stem].keys())}
    return sdict

def buildWordList(invertedIndex):
    wordList = []
    for word in invertedIndex.keys():
        wordList.append(word)
    return wordList

def writeToFile(data, filename):
    with open(filename, 'w') as write_f:
        json.dump(data, write_f, indent=4, ensure_ascii=False)
