import json
import hanlp


HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

def get_value(origin_list, label):
    token_list = origin_list["ner/msra"]
    result_str = ""
    for token in token_list:
        if token[1] == label:
            result_str += token[0]
    return result_str

def getKeywordsFromHanlp(filename):
    text = json.loads(open(f"data/{filename}", 'r').read())
    organization = get_value(HanLP(text["标题"], tasks="ner/msra"), 'ORGANIZATION')
    location_segment = text["文本"].split('：')[0]
    location = get_value(HanLP(location_segment, tasks="ner/msra"), 'LOCATION')
    time = text["时间"]
    strong = []
    try:
        strong = text["强调文本"]
    except:
        pass
    dict = {}
    dict["位置"] = location
    dict["时间"] = time
    dict["部门"] = organization
    dict["强调文本"] = strong
    return dict

