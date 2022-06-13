<div align='center' ><font size='70'>作业2 信息检索系统</font></div>

<div align=right>
    学号：2019211889&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;姓名：范学宇<br/>
	学号：2019211898&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;姓名：王天一
</div>

[TOC]

## 1 实验要求

#### 1.1 基本要求

- 数据源可以自选，数据通过开源的网络爬虫获取，规模不低于100篇文档，进行本地存储。
- 中文可以分词（可用开源代码），也可以不分词，直接使用字作为基本单元。英文可以直接通过空格分隔。
- 构建基本的倒排索引文件。
- 实现基本的向量空间检索模型的匹配算法。
- 用户查询输入可以是自然语言字串，查询结果输出按相关度从大到小排序，列出相关度、题目、主要匹配内容、URL、日期等信息。
- 最好能对检索结果的准确率进行人工评价。界面不做强制要求，可以是命令行，也可以是可操作的界面。

#### 1.2 扩展要求：

- 多媒体信息检索以及优化各模块算法。
- 算法评估、优化、论证创新点。

## 2 环境配置说明

1. pip安装paddlepaddle-tiny出现不能下载的问题。换用如下方式采用豆瓣源安装

```shell
pip3 install paddlepaddle -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
pip install protobuf==3.20
```

## 3 数据爬取

- 主题\类型：体育相关

- 爬取网站：[中国奥委会官方网站 (olympic.cn)](http://www.olympic.cn/news/olympic_comm/)

  ![image-20220613165918518](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655110765.png)

#### 3.1 核心代码:

  - 爬取数据主要使用lxml库，通过分析网页的xml，获取所需要的信息,然后将信息存入json格式文件中，方便之后分词，获取数据

  ```python
  response = requests.get(url_html, headers=headers, verify=False)
  response.encoding = 'utf-8'  # 更改编码 否则获取text乱码
  html = etree.HTML(response.text, etree.HTMLParser())
  try:
      title = html.xpath('/html/body/div[2]/div[4]/div[1]/div/h2/font/text()')[0] # 获取标题
      time = html.xpath('/html/body/div[2]/div[4]/div[1]/div/div[1]/div[1]/text()')[0] # 获取时间
      content_result = html.xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/p') # 获取正文
      content = []
      for p in content_result:
          content.append(p.xpath('./text()')[0])  # 获取到内容
      url = url_html # 获取url
  
      html_dict = getDict(title, time, '\n'.join(content), url) # 将以上信息转换为字典格式
      with open(f"{file_path}{'-'.join(time.split()).replace(':', '-')}.json", 'w') as write_f: # 存入json格式文件
          json.dump(html_dict, write_f, indent=4, ensure_ascii=False)
  
      except IndexError as e:
          print(e)
  ```


#### 3.2 本地文件样例:

  命名规则: YYYY-MM-DD-HH-MM

  存储信息:

  ```json
  {
  	"标题":"XXX",
  	"日期":"XXX",
  	"正文":"XXX",
  	"网址":"XXX"	
  }
  ```

  ![image-20220613020317348](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655057004.png)

## 4 中文分词

- 主要使用jieba中文分词库，使用函数jieba.cut()可以完成对中文文章的分词

- 分词样例

  ![image-20220613170800176](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655111280.png)

#### 4.1 核心代码

  定义getToken函数

  默认state=0，title=0，该状态下传入参数为文件名称，获取该文件内正文部分分词，返回分词后的list

  若state=0，title=1，该状态下传入参数为文件名称，获取该文件内标题部分分词，返回分词后的list

  若state=1，该状态下传入参数为字符串，即输入的待检索字符串，返回分词后的list

  ```python
  # 先前的代码不变，若需要使用getToken处理字面量，则给第二个参数赋转入非零值,第三个title用于获取标题分词
  def getToken(single_name, state=0, title=0):
      if state == 0:
          file_name = "data/" + single_name
          text = json.loads(open(file_name, 'r').read())
  
          if title:  # 对标题进行分词
              attribute = "标题"
              attribute_text = text[attribute]
          else:  # 对正文进行分词
              attribute = "正文"
              attribute_text = text[attribute]
      else:  # 对输入进行分词
          attribute_text = single_name
      attribute_text = re.sub('[\n\r\t]', '', attribute_text)
      return jieba.cut(attribute_text, use_paddle=True)
  
  
  def deduplicate(tokens):
      return set(tokens)
  ```

## 5 构建倒排索引

#### 5.1 倒排索引概念与原理

  倒排索引的英文原名是**Inverted index**，大概因为Invert有颠倒的意思，所以就被翻译成了倒排

  倒排索引源于实际应用中需要根据属性的值来查找记录，也就是说，不是由记录来确定属性值，而是由属性值来确定记录，因而称为**倒排索引**，

  建立全文索引中有两项非常重要，一个是对文本进行分词，一是建立索引的数据结构。

  一个未经处理的数据库中，一般是以文档ID作为索引，以文档内容作为记录。

  而Inverted index 是将单词作为索引，将文档ID作为记录，这样便可以方便地通过单词或记录查找到其所在的文档。

  1. 读取一整条句子到变量str中

  2. 从句子的尾端读取1个分词到变量word（单词）中

  3. 在字典查找word中保存的单词。如果不存在则保存word并转到步骤4，否则转到步骤5

  4. 如果是字典中最大单词或者超过最大单词数（认定为新词），从句尾去掉该单词，返回步骤2

  5. 继续读取前一个字到word中，转到步骤3

#### 5.2 倒排索引表结构

  由于篇幅原因具体表内容详见附件

  ```json
  {
    "word1":{
        "1":[2,5,8],
        "3":[3,6,9]
    },
    "word2":{
        "2":[15,36,50],
        "14":[6,23,41]
    }
    ···
  }
  ```

#### 5.3 核心代码

  将所有文章的标题和正文分别存储两个倒排索引表
  ```python
  def createIndex():
      index = {}
      index_title = {}
      files = os.listdir('data/')
      for file in files:
          doc_id = files.index(file)  # 获取文件的索引号
          content = getToken(file)  # 获取json文件内容
          title = getToken(file, title=1)  # 获取json文件标题
          index = getFlashBackTable(content, index, doc_id)
          index_title = getFlashBackTable(title, index_title, doc_id)
          
  def getFlashBackTable(content, index, doc_id):
      pos = 0  # 倒排索引表中 文档中位置
  
      for word in content:
          if word not in index:  # 若该分词不在索引表中，创建新的词典
              doc_list = {doc_id: [pos]}
              index[word] = doc_list
          else:
              if doc_id not in index[word]:  # 若该分词在索引表中，该词对应的文章号不存在，创建新list加入词典
                  index[word][doc_id] = [pos]
              else:  # 否则直接在list后面加入该分词位置即可
                  index[word][doc_id].append(pos)
          pos += 1
      return index
  ```


## 6 向量空间检索模型匹配算法

#### 6.1 向量空间检索模型原理

  - 优点

    相对于标准布尔模型，向量空间模型具有如下优点：
    
        1. 基于线性代数的简单模型
        2. 词组的权重不是二元的
        3. 文档和查询之间的相似度取值是连续的
        4. 允许根据文档间可能的相关性来进行排序
        5. 允许局部匹配
    
  - 局限

    1. 不适用于较长的文档，因为它的相似值不理想（过小的内积和过高的维数）。
    2. 检索词组必须与文档中出现的词组精确匹配；词语子字串可能会导致“假阳性”匹配。
    3. 语义敏感度不佳；具有相同的语境但使用不同的词组的文档不能被关联起来，导致“假阴性匹配”。
    4. 词组在文档中出现的顺序在向量形式中无法表示出来。
    5. 假定词组在统计上是独立的。
    6. 权重是直观上获得的而不够正式。
    
  - tf-idf

    - 概念

      **tf-idf**（英语：**t**erm **f**requency–**i**nverse **d**ocument **f**requency）是一种用于信息检索与文本挖掘的常用加权技术。tf-idf是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。
      
    - 原理
    
      在一份给定的文件里，**词频**（term frequency，tf）指的是某一个给定的词语在该文件中出现的频率。这个数字是对**词数**（term
      count）的归一化，以防止它偏向长的文件。（同一个词语在长文件里可能会比短文件有更高的词数，而不管该词语重要否。对于在某一特定文件里的词语 $t_i$ 来说，它的重要性可表示为：
    
      $\mathrm{tf}_{\mathrm{i}, \mathrm{j}}=\frac{n_{i, j}}{\sum_{k} n_{k, j}}$
    
      以上式子中$n_{i, j}$是该词在文件$d_j$中的出现次数，而分母则是在文件$d_j$中所有字词的出现次数之和。

      **逆向文件频率**（inverse documentfrequency，idf）是一个词语普遍重要性的度量。某一特定词语的idf，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取以10为底的对数得到：
      
      $\operatorname{idf}_{\mathrm{i}}=\lg \frac{|D|}{\left|\left\{j: t_{i} \in d_{j}\right\}\right|}$

      其中
    
        - |D|：语料库中的文件总数
        - $\left|\left\{j: t_{i} \in d_{j}\right\}\right|$包含词语的$t_i$文件数目（即$n_{i, j} \neq
          0$的文件数目）如果词语不在资料中，就导致分母为零，因此一般情况下使用$1+\left|\left\{j: t_{i} \in d_{j}\right\}\right|$
      
      然后 $$\operatorname{tfidf}_{\mathrm{i}, \mathrm{j}}=\mathrm{tf}_{\mathrm{i}, \mathrm{j}} \times \mathrm{idf}_
      {\mathrm{i}}$$
      
      某一特定文件内的高词语频率，以及该词语在整个文件集合中的低文件频率，可以产生出高权重的tf-idf。因此，tf-idf倾向于过滤掉常见的词语，保留重要的词语。
    
  - wf-idf

    总体原理与tf-idf相同，唯一区别是对tf做出了修改

    在文档中多次出现某个术语并不总是意味着与出现次数成比例的意义更大。 次线性tf标度是项频率的修改，其计算权重如下：

    $\mathrm{wf}_{t, d}=\left\{\begin{array}{ll}
    1+\log \mathrm{tf}_{t, d} & \text { if } \mathrm{tf}_{t, d}>0 \\
    0 & \text { otherwise }
    \end{array}\right.$

    在这种情况下，tf-idf变为：

    $\mathbf{wfidf_{t, d}}=\mathbf{w f}_{t, d} \times \mathrm{idf}_{t}$

#### 6.2 核心代码

  ```python
def getDataFilename(index, pieces):
    temp_list = []
    for piece in pieces:
        if piece in index:
            filename_list = [int(key) for key in index[piece].keys()]  # 查找对应文档对应的编号id
            # filename_list.sort() # 对文档编号排序
            temp_list.append(filename_list)
    list = [element for lis in temp_list for element in lis] # 将多个list压缩成一个list
    return sorted(set(list)) # list 去重然后排序
    
def getScoreList(index, file_num, pieces, file_list):
    score_list = []
    for file_id in file_list:
        WfIdfScore = getWfIdfScore(index, file_num, pieces, file_id)
        score_list.append([WfIdfScore, file_id])
    return sorted(score_list, reverse=True)
    
def getWfIdfScore(index, file_num, pieces, file_id):
    score = 0
    highlight = []
    file_id = str(file_id)
    for piece in pieces:# 依次对输入检索内容 去index里面匹配并计算得分
        if piece not in index or file_id not in index[piece]:
            continue
        tf = len(index[piece][file_id]) # 计算tf
        df = len(index[piece]) # 计算df
        wf = 1 + cmath.log10(tf).real # 计算wf 去除词频对匹配得分的影响
        idf = cmath.log10(file_num / df).real
        score += wf * idf
        highlight += index[piece][file_id] # 记录分词位置便于之后输出
    return [score, highlight]
  ```

## 7 结果展示

#### 7.1 核心代码

- 输出格式为：匹配得分序号，标题，日期，网址，wf-idf匹配程度，部分匹配内容

  ```python
  def printResult(reports, search_pieces, time_range, title_flag=0, content_flag=0):
      counter = 0
      for report in reports:
          file_name = id2name(report[1])
          full_path = "data/" + file_name
          text = json.loads(open(full_path, 'r',encoding='UTF-8').read())
          time = datetime.strptime(text["日期"], '%Y-%m-%d %H:%M')
  
          if len(time_range[0]) > 0 and time < datetime.strptime(time_range[0], '%y.%m.%d') or \
                  len(time_range[1]) > 0 and time > datetime.strptime(time_range[1], '%y.%m.%d'):
              continue
          counter += 1
          print(f'\033[1;30;47m{counter}\033[0m')
  
          # print(text["标题"])
          title_pieces = list(getToken(text["标题"], 1))
          # title_flag 为查询标题的标志，默认查询
          if not title_flag:
              print("标题: ", end="")
              for title_piece in title_pieces:
                  if title_piece in search_pieces:
                      print(f"\033[91m{title_piece}\033[0m", end="")
                  else:
                      print(title_piece, end="")
              print()
          else:
              print("标题: " + text["标题"])
  
          print("日期: " + text["日期"])
          print("网址: " + text["网址"])
          print("wf-idf匹配相关度: %.3f" % report[0][0])
  
          # content_flag 为查询正文的标志，默认查询
          if not content_flag:
              content = list(getToken(file_name))
              i = 0
              output_len = 0
              while i != len(content) and output_len <= 50:
                  if i in report[0][1]:
                      if output_len == 0 and i != 0: print('...', end='')
                      print(f'\033[91m{content[i]}\033[0m', end='')
                      output_len += len(content[i])
                  elif output_len > 0:
                      print(content[i], end='')
                      output_len += len(content[i])
                  i += 1
              if i != len(content): print('...', end='')
              print('\n')
      if counter == 0:
          print('\033[31m无匹配对象，请更换关键词或时间范围重试。\033[0m\n\n')
      else:
          print(f'\033[32m查找成功！共返回{counter}条结果。\033[0m\n\n')
  ```

#### 7.2 样例图片

![image-20220613040615956](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655064392.png)

![image-20220613040429973](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655064270.png)

## 8 使用说明

1. 启动程序，控制台输出"请选择查找模式"
2. 输入查找模式，然后控制台输出"请输入待查询语句"
3. 输入查询语句，然后控制台输出"输入查询时间"
4. 输入查询时间(可跳过，回车默认所有文档)
5. 控制台输出查询结果重回第一步循环执行

![image-20220613041537959](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655064938.png)

## 9 准确率与召回率

- 准确率

  该信息检索系统主要是基于倒排索引的向量空间检索模型，然后该系统在检索过程中并非严格索引，输入的自然语言字串进行分词后所有分词只要在任一文档中出现均会匹配成功，然而未匹配成功的均不会进行检索和输出，故检索准确率为100%，唯一的区别在于其wf-idf的分不同。

- 召回率

  该信息检索系统，无论是对于新闻文章的正文，还是标题，亦或是输入的自然语言字串，均是使用jieba库进行分词。所以对于所有相同或者类似词语句子的分词结果将相同。并且在写代码过程中验证确实如此。因此只要是输入与文章中出现类似含义的词语句子均会有相同分词，然后在经过倒排索引表检索，则所有文章均会被召回。

故该系统的准确率与召回率均维持在一个较高水平，可以满足信息检索的需求。经后期人工检查，分别检查了爬取文件和对应url的网站，准确率均为100%，召回率只要是能对语义进行正确分词即可满足要求的召回

## 10 算法优化

该信息检索系统主要算法为倒排索引和向量空间检索模型。而这两个算法均有各自的缺点，需要对其进行优化。

首先是倒排索引，倒排索引存在两个问题，1.倒排索引更新问题  2. 倒排索引文件较大问题

对于第一个问题，使用json格式可以完美解决，我们对data内文件与json文件的修改时间做比较，若data文件时间晚于json文件时间，则证明data文件做了修改，则只需要对该文件做倒排索引，然后与总倒排索引表合并即可。若是新插入文件也同理，新插入文件的修改时间必定晚于json文件，只需对其进行倒排索引即可，避免了每次更新数据集需要对所有数据进行一次倒排索引

- 核心代码

  ```python
  if not (os.path.exists('json/index.json') and os.path.exists('json/wordlist.json')):
      createIndex()
  else:# 若存在则比较更新时间  更新数据则进行更新index
      file_list = []
      for file in os.listdir('data/'):
          index_time = time.localtime(os.stat("json/index.json").st_mtime)
          data_time = time.localtime(os.stat(f"data/{file}").st_mtime)
          if index_time < data_time:
              file_list.append(file)
      for file in file_list:
          addIndex(file)
          
  #由于篇幅问题在此不展示addIndex函数源码
  #该函数主要是对需要加入倒排索引表中的文件单独进行倒排索引，然后再与index合并，避免了当更改数据需要全部更改索引表的问题
  ```

  

对于第二个问题，若倒排索引文件较大，可以采用类似词典的方式，但是这样词典方式对中文不太适合，虽然中文可以使用拼音来解决，但是这样又会增加内存空间的占用，最终的权衡下，因为文件数量毕竟有限，只是单一新闻网站新闻，未采用拼音加首字母方式加快索引

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/13/20220613-1655067414.png)

然后是向量空间检索模型，由于中文的特殊原因，中文分词会出现语气词和助词，而这些分词对于检索而言没有任何意义，只会产生干扰的索引结果

因此再计算向量空间检索得分时，我们摒弃了经常使用的tf-idf模型而是用了wf-idf模型，该模型的优点是削弱了词频带来的影响，当分词匹配程度不同时，匹配程度较高的文档才会有较高得分，在分词匹配程度相同时，词频较高的评分才会略有优势。具体算法与代码均在上述算法章节展示



















