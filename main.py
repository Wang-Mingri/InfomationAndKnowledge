import os.path, time

import spider
from InformationRetrieval.buildindex import *
from InformationRetrieval.getindex import *


def fun1(index, word_list,files, sentence):
    # TODO sentence分词  fenci(sentence)
    # TODO 将分词后去重，去杂（可不用）
    # TODO 获取所有分词结果所对应文档     wendang(index, pieces)
    # TODO 计算各个文档向量空间模型匹配程度  xiangliang(index, len(files), pieces, wendang)
    # TODO 对所有文档得分排序
    # TODO 输出前X项文档，得分，title，日期，url，匹配内容（有点难目前没思路）



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

    # 获取倒排索引表 index
    index = getIndex()
    # 获取倒排索引表词典 word_list
    word_list = getWordList()
    # 获取文件列表
    files = os.listdir('data/')

    print("************************************信息索引系统************************************")
    while True:
        print("请输入搜索模式： ")
        print("[1] 只在标题中， 只考虑正文， ")

        try:
            options = int(input())
            if options == 2:
                break
            if options > 2:
                print("输入数字不规范，重新输入")
                continue
        except:
            print("输入存在违法，请重新输入")
            continue

        print("请输入待查询语句:")
        sentence = input()

        if options == 1:
            fun1(index, word_list,files, sentence)





