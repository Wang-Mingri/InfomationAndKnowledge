import os

import spider
from InformationRetrieval import buildindex
from InformationRetrieval import getindex


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('./data/') | len(os.listdir('./data/')) > 100):
        spider()

    # 创建倒叙索引表
    buildindex()



