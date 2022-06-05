import os.path
import time

from IR.Spider import spider
from InformationRetrieval.VSM import *
from InformationRetrieval.createindex import *
from InformationRetrieval.tokens import *

# 获取输入
def getSentenceAndTimeRange():
    print("请输入待查询语句:")
    sentence = input()

    # TODO: 查询时间范围
    start_str = input("请输入查询起始时间:（仅接受格式为{year}.{month}.{day}的时间，回车跳过）")
    end_str = input("请输入查询终止时间:（仅接受格式为{year}.{month}.{day}的时间，回车跳过）")
    return sentence , [start_str, end_str]


# 获取信息索引内容
def getIR(index, files, sentence):
    pieces = getToken(sentence, 1)  # sentence分词
    # print(*pieces)
    pieces = deduplicate(pieces)
    # print(*pieces)
    file_list = getDataFilename(index, pieces)
    # print(*file_list)
    reports = getScoreList(index, len(files), pieces, file_list)

    return reports, pieces


# 在标题中或者正文中查找
def fun1(index, files, sentence, time_range):
    reports, pieces = getIR(index, files, sentence)
    printResult(reports, pieces, time_range)
    return


# 只在标题中查找
def fun2(index, files, sentence, time_range):
    reports, pieces = getIR(index, files, sentence)
    printResult(reports, pieces, time_range, content_flag=1)
    return


# 只在正文中查找
def fun3(index, files, sentence, time_range):
    reports, pieces = getIR(index, files, sentence)
    printResult(reports, pieces, time_range, title_flag=1)
    return


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()

    # 若不存在倒叙索引表 或者 创建时间早于data 则创建倒叙索引表
    if not os.path.exists('index.json') or not os.path.exists('wordlist.json'):
        createIndex()
    else:
        index_time = time.localtime(os.stat("wordlist.json").st_mtime)
        data_time = time.localtime(os.stat(f"data/{os.listdir('data/')[0]}").st_mtime)
        if index_time < data_time:
            createIndex()

    # 获取倒排索引表 index
    index = getIndex("json文件/index.json")
    index_title = getIndex("json文件/index_title.json")
    # 获取倒排索引表词典 word_list
    # word_list = getWordList("json文件/word_list.json")
    # word_list_title = geiWordList("json文件/word_list_title.json")
    # 获取文件列表
    files = os.listdir('data/')

    print("************************************信息索引系统************************************")
    while True:
        print("[1]:在标题和正文中查找， [2]:只在标题中查找， [3]:只在正文中查找, [4]:退出系统")
        print("请输入搜索模式: ")
        try:
            options = int(input())
            if options < 1 or options > 4:
                print("输入数字不规范，重新输入")
                continue
        except:
            print("输入存在违法，请重新输入")
            continue

        if options == 1:
            print("已进入在标题和正文中查找模式")
            sentence, time_range = getSentenceAndTimeRange()
            fun1(index, files, sentence, time_range)
        elif options == 2:
            print("已进入只在标题中查找模式")
            sentence, time_range = getSentenceAndTimeRange()

            fun2(index_title, files, sentence, time_range)
        elif options == 3:
            print("已进入只在正文中查找模式")
            sentence, time_range = getSentenceAndTimeRange()

            fun3(index, files, sentence, time_range)
        elif options == 4:
            print("感谢使用该信息检索系统")
            break
