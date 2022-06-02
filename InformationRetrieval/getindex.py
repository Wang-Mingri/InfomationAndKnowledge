import json

# 获取倒叙索引表
def getIndex():
    with open('/index.json', 'r') as index:
        index = json.load(index)
    return index

# 获取词项列表
def getWordList():
    with open('/wordlist.json', 'r') as word_list:
        word_list = json.load(word_list)
    return word_list