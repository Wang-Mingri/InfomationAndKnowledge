import hanlp
import json
hanlp.pretrained.mtl.ALL # MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

text = json.loads(open('../IR/data/2022-03-02-08-00.json', 'r').read())
doc = HanLP([text["正文"]], tasks='ner/ontonotes')
print(doc)
file = open("1text.txt", 'w')
file.write(str(doc))
file.close()