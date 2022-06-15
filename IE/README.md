*信息与知识获取*

# 实验三 信息抽取系统

[TOC]

## 一、信息抽取实验要求重述

- 基本要求：

  - 特定领域语料根据自己的兴趣选定，规模不低于100篇文档，进行本地存储。
  - 对自己感兴趣的特定信息点进行抽取，并将结果展示出来。
  - 其中，特定信息点的个数不低于5个。
  - 可以调用开源的中英文自然语言处理基本模块，如分句、分词、命名实体识别、句法分析。
  - 信息抽取算法可以根据自己的兴趣选择，至少实现正则表达式匹配算法的特定信息点抽取。
  - 最好能对抽取结果的准确率进行人工评价。
  - 界面可以是命令行，也可以是可操作的界面。

- 扩展要求：

  - 鼓励有兴趣和有能力的同学积极尝试多媒体信息抽取以及优化各模块算法，也可关注各类相关竞赛。
  - 算法评估、优化、论证创新点


## 二、信息抽取功能的设计思路

### 1. 信息抽取概念重述

- 文本信息抽取指的是这样一类文本处理技术，它从自然语言文本中自动抽取指定类型的实体（entity）、关系（relation）、事件（event）等事实信息，并形成结构化数据输出。

- 文本信息抽取主要包括三个方面的内涵：
  - 自动处理非结构化的自然语言文本；
  - 选择性抽取文本中指定的信息；
  - 就抽取的信息形成结构化数据表示。
- 考虑到携带信息的数据多种多样，我们可以从数据模型结构的规范化程度入手将其大致分为三种类型，即：结构化数据、非结构化数据和半结构化数据。

### 2. 信息抽取系统的数据选取思路及其特征介绍

#### (1) 数据获取途径

​	在上一个小节当中，我们对于信息抽取的**要旨**进行了重述。根据信息抽取所需解决的问题与面临的困难，**待分析的数据选取**就显得尤为重要。考虑到完成正则表达式匹配算法是本次课程的最低要求标准，换言之待分析的文本**至少当属半结构化数据**，我们经过对数十份开源爬虫项目进行评估和尝试后，在本次开发过程中**独立编写网络爬虫程序**，以更好地适应《信息与知识获取》课程学习与项目开发的需要。

> 特别地，我们会将**不涉及到本门课程教学核心内容**的网络爬虫程序于Github开源，在**不影响后续选修同学学习质量，保障学术诚信的前提下**助人少走弯路，以飨后来者。

#### (2) 数据选取对象

​	我们的数据采集对象是中国政府网平台“我向总理说句话”板块当中，关于网民留言的选登与解答的页面本文。下面给出示例页面快照。

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655104926.png" alt="image-20220613152205901" style="zoom:33%;" />

*图2-1 示例页面快照*

#### (3) 结合数据选取对象论述项目关于可持续发展的意义

​	对于人民群众而言，及时有效地向政府反馈基于社会实践所形成的改进建议历来当属历届政府、各地百姓高度重视的社会活动。国计民生当中相当一部分大事小情通过这一渠道进行反映、考察与着手解决。本次实验以此为案例进行分析的**出发点即是对于向社会施以可持续发展影响这一初衷。**通过我们的言传身教，以及在本实验所能指导的其他开发者与应用程序使用者群体当中，提高人们对参政议政的热情。

#### (4) 数据特征分析与执行效果示例

​	下面对于文本数据的特征进行分析，以第一页第一篇文本数据为例。

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655108275.png" alt="image-20220613161755286" style="zoom: 33%;" />

*图2-2 示例页面快照所显示出的待抽取信息点标注*

​	特定信息点包括如下8种：

1. 回复部门
2. 留言主题
3. 网友所在地
4. 网友网名
5. 网友联系方式
6. 供群众参考的法律法规与通知政策
7. 公开时间
8. 留言文本中强调部分

​	在这8种特定信息点当中，回复部门与留言主题采用分析文章标题的句法成分实现；网友相关信息与政策法规通过正则匹配算法实现；公开时间与强调文本则集成到网络爬虫爬取过程，通过对半结构化的html源代码进行分析得到。

​	我们在此对照原文展示示例网页信息抽取后的输出结果：

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655109138.png" alt="image-20220613163218313"/>

*图2-3 示例页面快照经抽取后的信息点输出*

**特别指出的是！这一部分会在算法优化部分再次提及，对于相关法律信息点的信息抽取会进行逻辑去重。**

#### (5) 关于人工评价的设计

​	如图1-3所示，在8个信息点输出完毕后另行输出了目标文本的url，以供使用者对照原文进行复核。

### 3. 运行环境

- 实验平台：Windows 10

- 使用工具：python 3.8.0

- 项目依赖：HanLP 2.1 (, Selenium, requests)

## 三、信息抽取功能的实现

### 1. 项目结构

```
IE
 ┗━ Spider
 	 ┗━ spider.py (存储网络爬虫程序)
 ┗━ data/ (存储网络爬虫获取数据)
 ┗━ InformationExtraction
 	 ┗━ regularmatch.py (实现正则匹配算法)
 	 ┗━ participle.py (实现句法分析)
 ┗━ result/ (存储信息抽取结果)
 ┗━ main.py (绘制命令行窗格，处理I/O交互，视项目数据目录的情况启动数据获取、信息抽取)
```

### 2. 关键代码说明

#### (a) 网络爬虫 spider.py

*鉴于文本中的两个信息点由爬虫分析半结构化文本直接获取，在此简略说明。*

​	时间与强调文本这两项信息点在半结构化数据格式特征突出，我们采用分析页面源码方式直接对于该特征进行捕获。以下是这两处信息点的获取逻辑

```python
time = browser.find_element(by=By.XPATH, value='//*[@class="pages-date"]').text[0:len("YYYY-MM-DD HH:MM")] # 获取文章时间
if time[0:2] == '20':
	dict["时间"] = time # 鉴于部分页面并不含有时间这一信息点，采用试探的方式进行确认

strong_list = span_list = []
try: # 获取文章加粗正文
    strong_pieces = browser.find_elements(by=By.TAG_NAME, value='strong') 
    strong_list = [piece.text for piece in strong_pieces]
except NoSuchElementException:
    pass
try:
    span_pieces = browser.find_elements(by=By.CSS_SELECTOR, value='span[style="font-weight: bold;"]')
    span_list = [piece.text for piece in span_pieces]
except NoSuchElementException:
    pass

if len(strong_list) + len(span_list) != 0:
    # dict["强调文本"] = '\n'.join(strong_list + span_list)
    dict["强调文本"] = strong_list + span_list
    # print(dict["强调文本"])
```

​	爬虫爬取结果存储范式为data/目录下对应网页索引位置存储的数个json文件，命名规则为：


```shell
[Page]_[Segment].json
```

​	数据存储格式规范为：

```json
{
    "标题": "XXX",
    "时间": "XXX", 
    "文本": "XXX", 
    "强调文本": [
        "XXX" ...
    ],
    "网址": "XXX"
}
```

​	下面给出示例输出的数据存储内容：

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655114073.png" alt="image-20220613175433661" style="zoom:50%;" />

*图3-1 示例页面的爬取结果本地保存格式*

#### (b) 句法分析 participle.py

​	句法分析抽取信息点部分使用了开源文本解析工具HanLP 2.1，通过对标题的句法分析分离出其中的句子成分并进行拆解，抽取出其中的信息点回复部门与留言主题。

​	下面展示程序核心部分：

```python
def get_value(origin_list, label):
    token_list = origin_list["ner/msra"]
    result_str = ""
    for token in token_list:
        if token[1] == label:
            result_str += token[0]
    return result_str


def getKeywordsFromHanlp(filename):
    text = json.loads(open(f"data/{filename}", 'r', encoding='UTF-8').read())
    organization = get_value(HanLP(text["标题"], tasks="ner/msra"), 'ORGANIZATION')
    location_segment = text["文本"].split('：')[0]
    location = get_value(HanLP(location_segment, tasks="ner/msra"), 'LOCATION')

    time = strong = []
    try:
        time = text["时间"]
    except:
        pass
    try:
        strong = text["强调文本"]
    except:
        pass

    url = text["网址"]
    dict = {"部门": organization, "强调文本": strong, "时间": time, "位置": location, "网址": url}
    return dict
```

#### (c) 正则匹配 regularmatch.py

​	正则匹配部分主要分析两部分内容，包括：留言开头部分关于网民情况介绍的语句，对其中的属地、网名以及联系方式信息进行提取；留言中双方所援引的政策通知与法律法规文本。

​	下面展示程序核心部分：

```python
def cut_sentences(content):
    sentences = re.split(r'(\!|\?|。|！|？|：|\n|\\)', content)
    return sentences


def regularmatch(filename):
    data = json.load(open(f"data/{filename}", "r", encoding='UTF-8'));
    content = cut_sentences(data["文本"])  # 对文本分句
    title = data["标题"]
    
    dir = {}
    dir["留言"] = re.match(r'.*[网关回局长][：民于应](.*)', title, re.M | re.I).group(1).lstrip('“').rstrip('” 题问的留言建议')
    dir["网名"] = []
    dir["手机尾号"] = []
    dir["相关法律"] = []
    for i in content:
        if re.match(r'.*网民“(.*)”.*', i, re.M | re.I) != None:
            dir["网名"].append(re.match(r'.*网民“(.*)”.*', i, re.M | re.I).group(1))  # 获取 网名
        elif re.match(r'(.*)说$', i, re.M | re.I) != None:
            dir["网名"].append(re.match(r'(.*)说$', i, re.M | re.I).group(1).strip())

        if re.match(r'.*手机尾号(.*)）.*', i, re.M | re.I) != None:
            dir["手机尾号"].append(re.match(r'.*手机尾号(.*)）.*', i, re.M | re.I).group(1))  # 获取手机尾号后四位

        if re.match(r'.*(《.*》).*', i, re.M | re.I) != None:
            dir["相关法律"].append(re.match(r'.*(《.*》).*', i, re.M | re.I).group(1))  # 获取 相关法律

    dir["相关法律"] = list(set(dir["相关法律"]))  # 去重

    return dir
```

#### (d) 主函数 main.py

​	主函数所完成的工作是读取项目根目录中的既有数据，判断当前系统是否需要爬取文本或更新信息抽取结果，确保信息抽取结果以既定格式存储。在完成数据分析后处理命令行的输入输出信息，对指定的数据区间进行输出。

##### i. 信息抽取结果输出

​	信息抽取的结果存储范式为result/目录下对应网页索引位置存储的数个json文件，命名规则为：


```shell
IE_[Page]_[Segment].json
```

​	数据存储格式规范为：

```json
{
    "留言": "XXX",
    "网名": [
        "XXX" ...
    ],
    "手机尾号": [
        "XXX" ...
    ],
    "相关法律": [
        "XXX" ...
    ],
    "部门": "XXX",
    "强调文本": [
        "XXX" ...
    ],
    "时间": "XXX",
    "位置": "XXX",
    "网址": "XXX"
}
```

​	下面给出示例输出的数据存储内容：

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655116001.png" alt="image-20220613182641670" style="zoom: 50%;" />

*图3-2 示例页面的信息抽取结果本地保存格式*

​	实现这一功能的核心代码如下：

```python
if __name__ == '__main__':
    # 若数据未爬取或者爬取文档数目小于100 重新爬取
    if not (os.path.exists('data/') and len(os.listdir('data/')) > 100):
        spider()

    if not (os.path.exists('result/') and len(os.listdir('result/')) == len(os.listdir('data/'))):
        dict = {}
        for filename in os.listdir('data/'):
            if os.path.exists(f'result/IE_{filename}'):
                continue
            dict = regularmatch(filename)
            dict.update(getKeywordsFromHanlp(filename))
            # for key, value in dict.items():
                # print('{key}:{value}'.format(key = key, value = value))
            with open(f"result/IE_{filename}", 'w', encoding='UTF-8') as write_f:
                json.dump(dict, write_f, indent=4, ensure_ascii=False)
```



---

##### ii. 命令行交互逻辑

​	在信息抽取的结果之上，通过用户指定页面输出范围实现交互。下面对于该环节进行演示：

- 错误输入

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655116760.png" alt="image-20220613183920466"  />

*图3-3-1 输入有误的情况*

- 单页查询正确输入

![image-20220613184139364](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655116899.png)

*图3-3-2 单页查询正确输入情况*

- 整页查询

![image-20220613184246696](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655116966.png)

*图3-3-3 整页查询情况*

- 重置与退出

![image-20220613184444618](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655117084.png)

*图3-3-4 重置与退出情况*

​	下面给出核心代码：

```python
def output(page, segment):
    print("信息点抽取开始:\n")
    if page == '':
        page_range = [1, 21]
    else:
        page_range = [int(page), int(page) + 1]
    if segment == '':
        segment_range = [1, 21]
    else:
        segment_range = [int(segment), int(segment) + 1]
    for page_num in range(*page_range):
        for seg_num in range(*segment_range):
            json_file = f'result/IE_{page_num}_{seg_num}.json'
            print(f"正在处理第{page_num}页第{seg_num}项")
            try:
                dict = json.loads(open(json_file, 'r', encoding='utf-8').read())
                print("信息点抽取结果如下:", end='\n\n')
                for key, value in dict.items():
                    value_str = ''
                    if isinstance(value, list):
                        value_str = '\n'.join(value)
                    elif isinstance(value, str):
                        value_str = value

                    if len(value_str) != 0:
                        print('\033[4m{a}\033[0m: {b}'.format(a=key, b=value_str))
                print()
            except FileNotFoundError:
                print(f"\n\033[31m未找到第{page_num}页第{seg_num}项")
                print("请更改目标重试\033[0m\n")
                return
    print("\033[32m输出完毕。\033[0m\n\n")
```

## 四、算法优化

### 1. 数据同步问题

​	与信息检索系统遇到的问题一致——在数据更新的情况下有必要对于修改进行同步，这种思想来源于Makefile分离编译的设计。

```python
dict = {}
for filename in os.listdir('data/'):
    if os.path.exists(f'result/IE_{filename}'):
        IE_time = time.localtime(os.stat(f"result/IE_{filename}").st_mtime)
        data_time = time.localtime(os.stat(f"data/{filename}").st_mtime)
        if IE_time > data_time:
            continue
    dict = regularmatch(filename)
    dict.update(getKeywordsFromHanlp(filename))
    # for key, value in dict.items():
    # print('{key}:{value}'.format(key = key, value = value))
    with open(f"result/IE_{filename}", 'w', encoding='UTF-8') as write_f:
        json.dump(dict, write_f, indent=4, ensure_ascii=False)
```

### 2. 表意重复问题

​	鉴于政府公文与通知中大量使用“以下简称”形式，如示例代码中的

```shell
……我们起草了《关于进一步做好阶段性价格临时补贴工作的通知》。这个《通知》近日已经印发各地。具体的工作安排，《通知》……
```

​	这一段内容，我们原先只做了同名的去重，但从语义上看三个文本的表意相同。考虑到这一点后，我们补充了对这种“以下简称”类型的去重，代码以及效果如下：

```python
dir["相关法律"] = list(set(dir["相关法律"]))  # 简单去重
for i in range(0, len(dir["相关法律"])):    # 逻辑去重
    for j in range(i + 1, len(dir["相关法律"])):
		if dir["相关法律"][j][1:-1] in dir["相关法律"][i][1:-1]:
            
            del dir["相关法律"][j]
            j -= 1
```

![image-20220613192218810](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/13/20220613-1655119339.png)

*图4-1 逻辑去重效果演示*