import cmath
import os
import json
from InformationRetrieval import tokens


# index 倒排索引 piece (2022年 北京 冬奥会)
def getDataFilename(index, pieces):
    temp_list = []
    for piece in pieces:
        if piece in index:
            filename_list = [int(key) for key in index[piece].keys()]  # 查找对应文档对应的编号id
            # filename_list.sort() # 对文档编号排序
            temp_list.append(filename_list)
    list = [element for lis in temp_list for element in lis]
    return sorted(set(list))


def getScoreList(index, file_num, pieces, file_list):
    score_list = []
    for file_id in file_list:
        WfIdfScore = getWfIdfScore(index, file_num, pieces, file_id)
        score_list.append([WfIdfScore, file_id])
    return sorted(score_list, reverse=True)


# 计算方法
# 首先对pieces中出现的单词对应的文档列表取并集。
# 随后对pieces中出现的单词对文档进行wf-idf计算并评分。
# 得到所有文档对该查询的评分后再对所有文档进行排序。
# wf-idf 和 tf-idf比较：
# 通过log计算削弱词项频率对评分的影响。
# 一篇文章中单词出现n次不代表其权重扩大n倍。
# 故采用wf-idf来计算
def getWfIdfScore(index, file_num, pieces, file_id):
    score = 0
    highlight = []
    file_id = str(file_id)
    for piece in pieces:
        if piece not in index or file_id not in index[piece]:
            continue
        tf = len(index[piece][file_id])
        df = len(index[piece])
        wf = 1 + cmath.log10(tf).real
        idf = cmath.log10(file_num / df).real
        score += wf * idf
        highlight += index[piece][file_id]
    return [score, highlight]


def id2name(file_id):
    path = 'data/'  # 获取文件路径
    files = os.listdir(path)
    return files[file_id]


# 文档，得分，title，日期，url，匹配内容
# reports [[ [score, highlight], file_id], ...]
def printResult(index, reports, search_pieces):
    results = []
    for report in reports:
        file_name = id2name(report[1])
        full_path = "data/" + file_name
        text = json.loads(open(full_path, 'r').read())

        print(file_name, report[0][0], end=' ')

        # print(text["标题"])
        title_pieces = list(tokens.getToken(text["标题"], 1))
        for title_piece in title_pieces:
            if title_piece in search_pieces:
                print(f'\033[91m{title_piece}\033[0m', end='')
            else:
                print(title_piece, end='')
        print('', end=' ')
        print(text["日期"], text["网址"])

        content = list(tokens.getToken(file_name))
        i = 0
        output_len = 0
        while i != len(content) and output_len <= 50:
            if i in report[0][1]:
                if output_len == 0 and i != 0: print('...', end='')
                print(f'\033[91m{content[i]}\033[0m', end='')
                output_len += len(content[i])
            elif output_len > 0:
                print(content[i], end='')
                output_len += len(content[i])
            i += 1
        if i != len(content): print('...', end='')
        print();print()
    if len(reports) == 0:
        print('\033[91m无匹配对象，请更换关键词重试\033[0m');print()