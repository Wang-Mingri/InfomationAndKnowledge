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
getToken(sentence, 1) # InformationRetrieval/tokens.py
```
- [x] 将分词后去重，去杂
```python
pieces = deduplicate(pieces) # InformationRetrieval/tokens.py
```
![image-20220604002400222](https://cdn.jsdelivr.net/gh/Wang-Mingri/Pic/PicGo/2022/06/04/20220604-1654273440.png)

- [ ] 获取所有分词结果所对应文档     wendang(index, pieces)
- [ ] 计算各个文档向量空间模型匹配程度  xiangliang(index, len(files), pieces, wendang)
- [ ] 对所有文档得分排序
- [ ] 输出前X项文档，得分，title，日期，url，匹配内容（有点难目前没思路）

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