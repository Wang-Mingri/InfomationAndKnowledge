import hanlp
import json
import os
from Spider.spider import *

def test():
    hanlp.pretrained.mtl.ALL # MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库

    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

    for page in range (15, 16):
        for section in range(1, 21):
            text = json.loads(open(f'data/{page}_{section}.json', 'r').read())
            organization = HanLP(text["标题"], tasks="ner/msra")["ner/msra"][0][0]
            # location = HanLP(text["文本"].split('\n'), tasks=)[]
            location_segment = text["文本"].split('：')[0]
            location = HanLP(location_segment, tasks="ner/msra")["ner/msra"]
            print(organization, location, end="\n\n-------------\n\n")
    # file = open("output.txt", 'w')
    # file.write(str(doc))
    # file.close()

if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    # if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
    #     spider()
    test()

def get_value(l, label):
