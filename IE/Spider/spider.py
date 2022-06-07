import requests
from lxml import etree
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import json

domain_name = "http://www.gov.cn"
content_label = "http://www.gov.cn/hudong/lkq_rdhy"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}

for page in range(1, 24):
    if page == 1:
        content_url = f"{content_label}.htm"
    else:
        content_url = f"{content_label}_{page}.htm"
    print(content_url)
    content_get = requests.get(content_url, headers=headers)
    content_html = etree.HTML(content_get.text, etree.HTMLParser())

    for i in range(1, 20):
        # print(i)
        # >>> print(html.xpath("/html/body/div[1]/div/div[2]/div[2]/ul/ul/li[1]/p[1]/a/@href")[0])
        # /hudong/2022-05/24/content_5692015.htm
        path = "/html/body/div[1]/div/div[5]/div[1]/ul" # /li[1]
        new_page_label = "/a/@href"
        # print(content_html.xpath(path + new_page_label))
        target_url = domain_name + str(content_html.xpath(f"{path}/li[{2*i-1}]{new_page_label}")[0])
        print(target_url)

        # target_get = requests.get(target_url, headers=headers)
        # target_html = etree.HTML(target_get.text, etree.HTMLParser())
        # target_label = '/html/body'
        # target_label = '/html/body/div[2]/div[1]/div[2]/div/div[2]'
        # print(target_html.xpath(target_label))
        # t = etree.tostring(target_html.xpath(target_label)[0], encoding="ascii", pretty_print=True)
        # print(t.decode("ascii"))

        # target_url = "http://www.gov.cn/hudong/2021-11/19/content_5651898.htm"
        browser = webdriver.Edge(service=Service("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"))
        browser.get(target_url)

        dict = {}
        title = browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div[2]/div/h1').text
        print(title)
        dict["标题"] = title

        text = browser.find_element(by=By.XPATH, value='//*[@id="UCAP-CONTENT"]').text
        print(text)
        dict["文本"] = text
        try:
            strong = browser.find_element(by=By.TAG_NAME, value='strong').text
            print(strong)
            dict["强调文本"] = strong
        except NoSuchElementException:
            pass

        with open(f"{page}_{i}json", 'w') as write_f:
            json.dump(dict, write_f, indent=4, ensure_ascii=False)

browser.close()
print("生成成功！")