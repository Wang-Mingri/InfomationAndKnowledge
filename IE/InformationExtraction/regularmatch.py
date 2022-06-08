import re
import json


def cut_sentences(content):
    sentences = re.split(r'(\!|\?|。|！|？|：|\n)', content)
    return sentences


def regularmatch(filename):
    data = json.load(open(f"data/{filename}", "r"));
    content = cut_sentences(data["文本"]) # 对文本分句
    dir = {}
    dir["网名"] = []
    dir["相关法律"] = []
    dir["手机尾号"] = []
    for i in content:
        if re.match(r'.*网民“(.*)”.*', i, re.M | re.I)!= None:
            dir["网名"].append(re.match(r'.*网民“(.*)”.*', i, re.M | re.I).group(1)) # 获取 网名
        elif re.match( r'(.*)$说', i, re.M|re.I)!= None:
            dir["网名"].append(re.match( r'(.*)$说', i, re.M|re.I).group(1))

        if re.match( r'.*(《.*》).*', i, re.M|re.I)!= None:
            dir["相关法律"].append(re.match( r'.*(《.*》).*', i, re.M|re.I).group(1)) # 获取 相关法律
        if re.match(r'.*手机尾号(.*)）.*', i, re.M | re.I)!= None:
            dir["手机尾号"].append(re.match(r'.*手机尾号(.*)）.*', i, re.M | re.I).group(1)) # 获取手机尾号后四位

    dir["相关法律"] = list(set(dir["相关法律"])) #  去重
    return dir



# 获取 相关法律
# line = "014年2月，国务院印发了《注册资本登记制度改革方案》（国发〔2014〕7号）"
# matchObj = re.match( r'.*(《.*》).*', line, re.M|re.I)
# if matchObj:
#     print ("matchObj.group() : ", matchObj.group())
#     print ("matchObj.group(1) : ", matchObj.group(1))
# else:
#     print ("No match!!")


# 获取 网名
# line = "丽丽说：我是一名下岗职工，"
# matchObj = re.match( r'(.*)说：.*', line, re.M|re.I)
# if matchObj:
#     print ("matchObj.group() : ", matchObj.group())
#     print ("matchObj.group(1) : ", matchObj.group(1))
# else:
#     print ("No match!!")


# 获取手机尾号后四位
# line = "来自江苏苏州的网民“华庆春”（手机尾号2715）说,来自湖北恩施的网民“小朵”（手机尾号5782）说"
# matchObj = re.match(r'.*手机尾号(.*)）.*', line, re.M | re.I)
# if matchObj:
#     print("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(1) : ", matchObj.group(1))
# else:
#     print("No match!!")
