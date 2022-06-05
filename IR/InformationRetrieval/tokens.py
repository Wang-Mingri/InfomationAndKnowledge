# encoding=utf-8
import jieba
import json
import logging
import re
# import stanza


# diction_path = "IE/diction.txt"
# jieba.load_userdict(diction_path)

jieba.setLogLevel(logging.INFO)


# 先前的代码不变，若需要使用getToken处理字面量，则给第二个参数赋转入非零值,title用于获取标题分词
def getToken(single_name, state=0, title=0):
    if state == 0:
        file_name = "data/" + single_name
        text = json.loads(open(file_name, 'r').read())

        if title:
            attribute = "标题"
            attribute_text = text[attribute]
        else:
            attribute = "正文"
            attribute_text = text[attribute]
    else:
        attribute_text = single_name
    # print(*text)
    attribute_text = re.sub('[\n\r\t]', '', attribute_text)

    # attribute_text = re.sub('[“”‘’、()《》 ]', '', attribute_text)
    # # print(attribute_text)
    # segment_list = re.split('[，,。：；\n\r\t]', attribute_text)
    # while '' in segment_list:
    #     segment_list.remove('')
    # # print(*segment_list)
    #
    # result = []
    # for segment in segment_list:
    #     # print(segment)
    #     token_list = jieba.cut(segment, use_paddle=True)
    #     # token_list = zh_nlp(segment)
    #     # print(*token_list)
    #     result += token_list
    # # print(*result)

    return jieba.cut(attribute_text, use_paddle=True)


def deduplicate(tokens):
    return set(tokens)
