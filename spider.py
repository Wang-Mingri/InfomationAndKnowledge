import json
import warnings

import requests
import re
import pandas as pd
from lxml import etree
import numpy as np
from matplotlib import pyplot as plt
import os

# 忽略运行过程中的warning
warnings.filterwarnings('ignore')

# 设置对中文的支持
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

file_path = 'data/'


# 对目录页面索引，寻找所需要内容网页的网址
def getURL(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'}

    response = requests.get(url, headers=headers, verify=False)
    html = etree.HTML(response.text, etree.HTMLParser())
    result = html.xpath('/html/body/div/div[4]/div[1]/div[1]/ul/li')
    html_list = []

    for li in result:
        html_list.append(li.xpath('./a/@href')[0])

    return html_list


# 将获取数据转换为字典
def getDict(title, time, content, url):
    dict = {}
    dict['标题'] = title
    dict['日期'] = time.strip()
    dict['正文'] = content.replace('\r\n\t\u3000\u3000', '')
    dict['网址'] = url
    return dict


# 获取页面内容
def getArticle(url_html):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'}
    response = requests.get(url_html, headers=headers, verify=False)
    response.encoding = 'utf-8'  # 更改编码 否则获取text乱码
    html = etree.HTML(response.text, etree.HTMLParser())
    try:
        title = html.xpath('/html/body/div[2]/div[4]/div[1]/div/h2/font/text()')[0]
        time = html.xpath('/html/body/div[2]/div[4]/div[1]/div/div[1]/div[1]/text()')[0]
        content_result = html.xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/p')
        content = []
        for p in content_result:
            content.append(p.xpath('./text()')[0])  # 获取到内容
        url = url_html

        html_dict = getDict(title, time, '\n'.join(content), url)
        with open(f"{file_path}{'-'.join(time.split()).replace(':', '-')}.json", 'w') as write_f:
            json.dump(html_dict, write_f, indent=4, ensure_ascii=False)

    except IndexError as e:
        print(e)


def spider():
    init_url = 'http://www.olympic.cn/news/olympic_comm/'
    for i in range(1, 10):
        tail = f'list_407_{i}.html'
        html_list = getURL(init_url + tail)
        for j in html_list:
            getArticle(j)

