# encoding=utf-8

import json
import jieba
import re
import logging
# import stanza


# diction_path = "./diction.txt"
# jieba.load_userdict(diction_path)

jieba.setLogLevel(logging.INFO)


def getToken(single_name):

    file_name = "./data/" + single_name

    # file_name = "data/2022-03-02-07-59.json"
    text = json.loads(open(file_name, 'r').read())
    # print(*text)
    result = []

    attribute = "正文"
    attribute_text = text[attribute]
    attribute_text = re.sub('[“”‘’、()《》 ]', '', attribute_text)
    # print(attribute_text)
    segment_list = re.split('[，,。：；\n\r\t]', attribute_text)
    while '' in segment_list:
        segment_list.remove('')
    # print(*segment_list)

    for segment in segment_list:
        # print(segment)
        token_list = jieba.cut(segment, use_paddle=True)
        # token_list = zh_nlp(segment)
        # print(*token_list)
        result += token_list
    print(*result)
    return result


