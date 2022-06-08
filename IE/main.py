import hanlp
import json
import os
from Spider.spider import *
from InformationExtraction.participle import *


def get_value(origin_list, label):
    token_list = origin_list["ner/msra"]
    result_str = ""
    for token in token_list:
        if token[1] == label:
            result_str += token[0]
    return result_str


def test():
    hanlp.pretrained.mtl.ALL  # MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库

    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

    for page in range(1, 16):
        for section in range(1, 21):
            text = json.loads(open(f'data/{page}_{section}.json', 'r').read())
            organization = get_value(HanLP(text["标题"], tasks="ner/msra"), 'ORGANIZATION')
            location_segment = text["文本"].split('：')[0]
            location = get_value(HanLP(location_segment, tasks="ner/msra"), 'LOCATION')
            time = text["时间"]
            strong = ""
            try:
                strong = text["强调文本"]
            except:
                pass
            print(f"Processing Page{page} Section{section}", organization, location, time, strong, end="\n\n-------------\n\n")


if __name__ == '__main__':
    test()
    # # 若数据未爬取或者爬取文档数目小于100 重新爬取
    # if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
    #     spider()
    for i in os.listdir('data/'):
        regularmatch(i)

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


