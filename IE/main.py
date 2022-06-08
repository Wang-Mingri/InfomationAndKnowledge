import hanlp
import json
import os
from Spider.spider import *

def test():
    text = json.loads(open('data/2_3.json', 'r').read())
    PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
    analyzer = PerceptronLexicalAnalyzer()
    print(analyzer.analyze(text["文本"]))


if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') | len(os.listdir('data/')) > 100):
        spider()
    # test()