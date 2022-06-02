# encoding=utf-8
import json
# import jieba
import stanza
import re
import os


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('data/2022-03-02-07-59.json'):
                fullname = os.path.join(root, f)
                yield fullname


def test():
    data_folder = "./data"
    stanza.download('zh')
    zh_nlp = stanza.Pipeline('zh', use_gpu=False)

    for file_name in findAllFile(data_folder):
        # file_name = "data/2022-03-02-07-59.json"
        text = json.loads(open(file_name, 'r').read())
        # print(*text)

        attribute = "正文"
        attribute_text = text[attribute]
        attribute_text = re.sub('[“”‘’、()]', '', attribute_text)
        # print(attribute_text)
        segment_list = re.split('[，,。：；\n\r\t]', attribute_text)
        while '' in segment_list:
            segment_list.remove('')
        print(*segment_list)

        for segment in segment_list:
            # print(segment)
            # token_list = jieba.cut(segment, use_paddle=True)
            token_list = zh_nlp(segment)
            print(*token_list)
            # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式


if __name__ == "__main__":
    # diction_path = "./diction.txt"
    # jieba.load_userdict(diction_path)

    test()

