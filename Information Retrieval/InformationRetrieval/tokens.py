# encoding=utf-8

import json
import jieba
import re
import logging

# import stanza


# diction_path = "InformationRetrieval/diction.txt"
# jieba.load_userdict(diction_path)

jieba.setLogLevel(logging.INFO)


# 先前的代码不变，若需要使用getToken处理字面量，则给第二个参数赋转入非零值
def getToken(single_name, state=0):
    if state == 0:
        file_name = "data/" + single_name
        # file_name = "data/2022-03-02-07-59.json"
        text = json.loads(open(file_name, 'r').read())

        # attribute_text = ''
        # if arrange | 2:
        #     attribute = "标题"
        #     attribute_text += text[attribute]
        # if arrange | 1:
        #     attribute = "正文"
        #     attribute_text += text[attribute]
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

if __name__ == '__main__':
    print(*getToken('2022-03-01-10-04.json'))