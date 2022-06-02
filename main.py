import os.path, time

import spider
from InformationRetrieval.buildindex import *
from InformationRetrieval.getindex import *


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()

    # 若不存在倒叙索引表 或者 创建时间早于data 则创建倒叙索引表
    if not (os.path.exists('index.json') | os.path.exists('wordlist.json')):
        buildIndex()
    else:
        index_time = time.localtime(os.stat("wordlist.json").st_mtime)
        data_time = time.localtime(os.stat(f"data/{os.listdir('data/')[0]}").st_mtime)
        if index_time < data_time:
            buildIndex()

    index = getIndex()
    worl_list = getWordList()


