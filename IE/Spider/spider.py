import os
import requests
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import json


def spider():
    domain_name = "http://www.gov.cn"
    content_label = "http://www.gov.cn/hudong/lkq_rdhy"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}

    print("开始爬取数据")
    for page in range(1, 24):
        if page == 1:
            content_url = f"{content_label}.htm"
        else:
            content_url = f"{content_label}_{page}.htm"
        content_get = requests.get(content_url, headers=headers)
        content_html = etree.HTML(content_get.text, etree.HTMLParser())

        for i in range(1, 20):
            # 可检测文章是否存在若存在则跳过
            if os.path.exists(f"data/{page}_{i}.json"):
                continue
            # print(i)
            # >>> print(html.xpath("/html/body/div[1]/div/div[2]/div[2]/ul/ul/li[1]/p[1]/a/@href")[0])
            # /hudong/2022-05/24/content_5692015.htm
            path = "/html/body/div[1]/div/div[5]/div[1]/ul" # /li[1]
            new_page_label = "/a/@href"
            target_url = domain_name + str(content_html.xpath(f"{path}/li[{2*i-1}]{new_page_label}")[0])# 获取文章的url

            # 使用selenium自动化抓取文章内容
            edge_options = Options()
            edge_options.add_argument('--headless')
            browser = webdriver.Edge(
                service=Service("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"),
                options=edge_options)
            browser.get(target_url)

            dict = {}
            dict["标题"] = browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div[2]/div/h1').text # 获取文章标题
            dict["时间"] = browser.find_element(by=By.XPATH, value='//*[@class="pages-date"]').text[0:len("YYYY-MM-DD HH:MM")] # 获取文章时间
            dict["文本"] = browser.find_element(by=By.XPATH, value='//*[@id="UCAP-CONTENT"]').text # 获取文章正文
            try:
                dict["强调文本"] = browser.find_element(by=By.TAG_NAME, value='strong').text # 获取文章加粗正文
            except NoSuchElementException:
                pass

            with open(f"data/{page}_{i}.json", 'w') as write_f:
                json.dump(dict, write_f, indent=4, ensure_ascii=False)

    browser.close()
    print("生成成功！")