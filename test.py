# encoding=utf-8
import json

import jieba
import re
import os


# import paddle

# paddle.enable_static()
#
# jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
# strs = ["我来到北京清华大学", "乒乓球拍卖完了", "中国科学技术大学"]
# for str in strs:
#     seg_list = jieba.cut(str, use_paddle=True)  # 使用paddle模式
#     print("Paddle Mode: " + '/'.join(list(seg_list)))
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('04.json'):
                fullname = os.path.join(root, f)
                yield fullname


def test():
    data_folder = "data"

    for file_name in findAllFile(data_folder):
        # file_name = "data/2022-03-02-07-59.json"
        text = json.loads(open(file_name, 'r').read())
        # print(*text)

        attribute = "正文"
        attribute_text = text[attribute]
        attribute_text = re.sub('[“”‘’、()]', '', attribute_text)
        # print(attribute_text)
        token_list = re.split('[，,。：；\n\r]', attribute_text)
        while '' in token_list:
            token_list.remove('')

        for token in token_list:
            # print(token)
            seg_list = jieba.cut(token, use_paddle=True)
            print(*seg_list)
            # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式


if __name__ == "__main__":
    test()
