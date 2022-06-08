import json
import os
from Spider.spider import *
from InformationExtraction.participle import *
from InformationExtraction.regularmatch import *

if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()

    dict = {}
    for filename in os.listdir('data/'):
        dict = regularmatch(filename)
        dict.update(getKeywordsFromHanlp(filename))
        with open(f"result/{filename}_IE.json", 'w') as write_f:
            json.dump(dict, write_f, indent=4, ensure_ascii=False)


    # # TODO 分词输出到 json文件
    # for i in range (len(os.listdir('data/'))):
    #     participle(filename)
    #
    # # TODO 从json文件中获取数据 正则匹配 输出到 result 格式如第三个todo
    # for i in range(len(os.listdir('json文件/'))):
    #     regularmatch(filename)
    #
    # # TODO 输出result
    # # json文件filename：？？？if or not
    # # 留言关键词：
    # # 留言人地区：
    # # 留言时间：
    # # 政府部门类别：
    # # 相关法律法规：
    # # 具体解决方法：
