import cmath
import os
import json

def getDataFilename(index, pieces):
    temp_list = []
    for piece in pieces:
        filename_list = []
        if piece not in index:
            temp_list.append(filename_list)
        else:
            filename_list = [int(key) for key in index[piece].keys()] # 查找对应文档对应的编号id
            filename_list.sort() # 对文档编号排序
            temp_list.append(filename_list)
    list = []
    for i in temp_list:
        list += i
    return sorted(set(list))

def getScoreList(index, file_num, pieces, file_list):
    score_list = []
    for file_id in file_list:
        score = getWfIdfScore(index, file_num, pieces, file_id)
        score_list.append([score, file_id])
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
    file_id = str(file_id)
    for piece in pieces:
        if piece not in index or file_id not in index[piece]:
            continue
        tf = len(index[piece][file_id])
        df = len(index[piece])
        wf = 1 + cmath.log10(tf).real
        idf = cmath.log10(file_num / df).real
        score += wf * idf
    return score

def id2name(file_id):
    path = 'data/'  # 获取文件路径
    files = os.listdir(path)
    return files[file_id]

# 文档，得分，title，日期，url，匹配内容
# reports [[score, file_id], ...]
def getResult(index, reports):
    results = []
    for report in reports:
        file_name = id2name(report[1])
        full_path = "data/" + file_name
        text = json.loads(open(full_path, 'r').read())

        results.append([file_name, report[0], text["标题"], text["日期"], text["网址"]])
