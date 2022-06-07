import hanlp
import json
import os
from Spider.spider import *

def test():
    hanlp.pretrained.mtl.ALL # MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库

    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

    text = json.loads(open('../IR/data/2022-03-02-08-00.json', 'r').read())
    doc = HanLP([text["正文"]], tasks='ner/ontonotes')
    print(doc)
    file = open("1text.txt", 'w')
    file.write(str(doc))
    file.close()

if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()