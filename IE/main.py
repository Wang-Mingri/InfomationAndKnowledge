import json
import os
from Spider.spider import *
from InformationExtraction.participle import *
from InformationExtraction.regularmatch import *

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)


def get_value(origin_list, label):
    token_list = origin_list["ner/msra"]
    result_str = ""
    for token in token_list:
        if token[1] == label:
            result_str += token[0]
    return result_str


def getKeywordsFromHanlp(filename):
    text = json.loads(open(filename, 'r').read())
    organization = get_value(HanLP(text["标题"], tasks="ner/msra"), 'ORGANIZATION')
    location_segment = text["文本"].split('：')[0]
    location = get_value(HanLP(location_segment, tasks="ner/msra"), 'LOCATION')
    time = text["时间"]
    strong = []
    try:
        strong = text["强调文本"]
    except:
        pass
    print(f"Processing Page Section", end='\n\n')
    return [organization, location, time, strong]


def output(json_file):
    try:
        dict = json.loads(open(json_file, 'r').read())
        print("信息点抽取结果如下:", end='\n\n')
        for key, value in dict.items():
            value_str = ''
            if isinstance(value, list):
                value_str = '\n'.join(value)
            elif isinstance(value, str):
                value_str = value

            if len(value_str) != 0:
                print('\033[4m{a}\033[0m:{b}'.format(a=key, b=value_str))
        print("\n\033[32m输出完毕。\033[0m\n\n")
    except FileNotFoundError:
        print(f"\n\033[31m未找到目标文件: json_file")
        print("请更改目标重试\033[0m\n")


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    # if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
    #     spider()

    dict = {}
    for filename in os.listdir('data/'):
        dict = regularmatch(filename)
        dict.update(getKeywordsFromHanlp(filename))
        with open(f"result/{filename}_IE.json", 'w') as write_f:
            json.dump(dict, write_f, indent=4, ensure_ascii=False)


    print("************************************信息抽取系统************************************")
    while True:
        page = input("请输入待抽取文本所在页码(回车代表对所有页面进行查询): ")
        segment = input("请输入指定页面上的待抽取文件所在位置(回车代表对指定页面所有项目进行查询): ")
        output(f'result/IE_{page}_{segment}.json')
