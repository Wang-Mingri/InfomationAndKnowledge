import os.path, time

import spider
from InformationRetrieval.buildindex import *
from InformationRetrieval.tokens import *
from InformationRetrieval.VSM import *


def fun1(index, files, sentence, time_range):
    pieces = getToken(sentence, 1)  # sentence分词
    # print(*pieces)
    pieces = deduplicate(pieces)
    # print(*pieces)
    file_list = getDataFilename(index, pieces)
    # print(*file_list)
    reports = getScoreList(index, len(files), pieces, file_list)
    printResult(reports, pieces, time_range)
    return


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()

    # 若不存在倒叙索引表 或者 创建时间早于data 则创建倒叙索引表
    if not os.path.exists('index.json') or not os.path.exists('wordlist.json'):
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

        # print("请输入搜索模式： ")
        # print("[1] 只在标题中， 只考虑正文， ")
        #
        # try:
        #     options = int(input())
        #     if options == 2:
        #         break
        #     if options > 2:
        #         print("输入数字不规范，重新输入")
        #         continue
        # except:
        #     print("输入存在违法，请重新输入")
        #     continue
        if True:  # FIXME: 改一下逻辑 测试环节太难受了
            options = 1
            print("已进入只在正文查找模式")

        print("请输入待查询语句:")
        sentence = input()

        # TODO: 查询时间范围
        start_str = input("请输入查询起始时间:（仅接受格式为{year}.{month}.{day}的时间，回车跳过）")
        end_str = input("请输入查询终止时间:（仅接受格式为{year}.{month}.{day}的时间，回车跳过）")

        if options == 1:
            fun1(index, files, sentence, [start_str, end_str])
