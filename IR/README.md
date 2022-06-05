# InfomationAndKnowledge

## 环境配置说明

1. pip安装paddlepaddle-tiny出现不能下载的问题。换用如下方式采用豆瓣源安装

```shell
pip3 install paddlepaddle -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
pip install protobuf==3.20
```

## 作业2 信息检索系统

- 数据源可以自选，数据通过开源的网络爬虫获取，规模不低于100篇文档，进行本地存储。
- 中文可以分词（可用开源代码），也可以不分词，直接使用字作为基本单元。英文可以直接通过空格分隔。
- 构建基本的倒排索引文件。
- 实现基本的向量空间检索模型的匹配算法。
- 用户查询输入可以是自然语言字串，查询结果输出按相关度从大到小排序，列出相关度、题目、主要匹配内容、URL、日期等信息。
- 最好能对检索结果的准确率进行人工评价。界面不做强制要求，可以是命令行，也可以是可操作的界面。

#### 扩展要求：

- 多媒体信息检索以及优化各模块算法。
- 算法评估、优化、论证创新点。

### main.fun1()

- [x] sentence分词

```python
# 先前的代码不变，若需要使用getToken处理字面量，则给第二个参数赋转入非零值
getToken(sentence, 1)  # IE/tokens.py
```

- [x] 将分词后去重，去杂

```python
pieces = deduplicate(pieces)  # IE/tokens.py
```

![image-20220604002400222](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/04/20220604-1654273440.png)

- [x] 获取所有分词结果所对应文档 wendang(index, pieces)

```python
getDataFilename(index, pieces)
```

- [x] 计算各个文档向量空间模型匹配程度&对所有文档得分排序 xiangliang(index, len(files), pieces, wendang)

```python
getScoreList(index, file_num, pieces, file_list)
```

- [x] 输出前X项文档，得分，title，日期，url，匹配内容

<img src="https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/04/20220604-1654323874.png" alt="image-20220604142434131" style="zoom:50%;" />

---

主题\类型：？

爬取网站：？

信息检索：

要求：

构建基本的倒排索引文件。实现基本的向量空间检索模型的匹配算法。

用户查询输入可以是自然语言字串，查询结果输出按相关度从大到小排序，列出相关度、题目、主要匹配内容、URL、日期等信息。

- 向量空间模型

  ![image-20220601231639310](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096606.png)

  ![image-20220601231658255](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096618.png)

  ![image-20220601231734750](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096654.png)

  ![image-20220601231809052](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096689.png)

  ![image-20220601231825071](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096705.png)

  ![image-20220601231837894](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096717.png)

    - 优点

      相对于[标准布尔模型](https://zh.wikipedia.org/w/index.php?title=标准布尔模型&action=edit&redlink=1)（Standard Boolean
      model），向量空间模型具有如下优点：

        1. 基于线性代数的简单模型
        2. 词组的权重不是二元的
        3. 文档和查询之间的相似度取值是连续的
        4. 允许根据文档间可能的相关性来进行排序
        5. 允许局部匹配

    - 局限

        1. 不适用于较长的文档，因为它的相似值不理想（过小的[内积](https://zh.wikipedia.org/wiki/内积)和过高的维数）。
        2. 检索词组必须与文档中出现的词组精确匹配；词语[子字串](https://zh.wikipedia.org/w/index.php?title=子字串&action=edit&redlink=1)
           可能会导致“[假阳性](https://zh.wikipedia.org/wiki/假陽性)”匹配。
        3. 语义敏感度不佳；具有相同的语境但使用不同的词组的文档不能被关联起来，导致“假阴性匹配”。
        4. 词组在文档中出现的顺序在向量形式中无法表示出来。
        5. 假定词组在统计上是独立的。
        6. 权重是直观上获得的而不够正式。

    - tf-idf

        - 概念

          **tf-idf**（英语：**t**erm **f**requency–**i**nverse **d**ocument **f**
          requency）是一种用于[信息检索](https://zh.wikipedia.org/wiki/資訊檢索)与[文本挖掘](https://zh.wikipedia.org/wiki/文本挖掘)
          的常用加权技术。tf-idf是一种统计方法，用以评估一字词对于一个文件集或一个[语料库](https://zh.wikipedia.org/wiki/語料庫)
          中的其中一份[文件](https://zh.wikipedia.org/wiki/文件)的重要程度。字词的重要性随着它在文件中出现的次数成[正比](https://zh.wikipedia.org/wiki/正比)
          增加，但同时会随着它在语料库中出现的频率成反比下降。

        - 原理

          在一份给定的文件里，**词频**（term frequency，tf）指的是某一个给定的词语在该文件中出现的频率。这个数字是对**词数**（term
          count）的归一化，以防止它偏向长的文件。（同一个词语在长文件里可能会比短文件有更高的词数，而不管该词语重要与否。）对于在某一特定文件里的词语 $t_i$ 来说，它的重要性可表示为：

          $\mathrm{tf}_{\mathrm{i}, \mathrm{j}}=\frac{n_{i, j}}{\sum_{k} n_{k, j}}$

          以上式子中$n_{i, j}$是该词在文件$d_j$中的出现次数，而分母则是在文件$d_j$中所有字词的出现次数之和。

          **逆向文件频率**（inverse document
          frequency，idf）是一个词语普遍重要性的度量。某一特定词语的idf，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取以10为底的[对数](https://zh.wikipedia.org/wiki/對數)
          得到：

          $\operatorname{idf}_{\mathrm{i}}=\lg \frac{|D|}{\left|\left\{j: t_{i} \in d_{j}\right\}\right|}$

          其中

            - |D|：语料库中的文件总数
            - $\left|\left\{j: t_{i} \in d_{j}\right\}\right|$包含词语的$t_i$文件数目（即$n_{i, j} \neq
              0$的文件数目）如果词语不在资料中，就导致分母为零，因此一般情况下使用$1+\left|\left\{j: t_{i} \in d_{j}\right\}\right|$

          然后

          $\operatorname{tfidf}_{\mathrm{i}, \mathrm{j}}=\mathrm{tf}_{\mathrm{i}, \mathrm{j}} \times \mathrm{idf}_
          {\mathrm{i}}$

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


- 倒排索引机制

  ![image-20220601232012296](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096812.png)

  ![image-20220601232022149](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096822.png)

  ![image-20220601232054253](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096854.png)

  ![image-20220601232126364](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096886.png)

![image-20220601232206053](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096926.png)

![image-20220601232236562](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654096956.png)

信息抽取：

- ![image-20220601232646088](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654097206.png)
- ![image-20220601232704096](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654097224.png)
- ![image-20220601232718925](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654097238.png)
- ![image-20220601232744093](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654097264.png)
- ![image-20220601232807354](https://cdn.jsdelivr.net/gh/Arete-FFF/PicGo/images/2022/06/01/20220601-1654097287.png)