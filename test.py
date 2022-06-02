# coding utf-8
import stanza

# 可以通过pipeline预加载不同语言的模型，也可以通过pipeline选择不同的处理模块，还可以选择是否使用GPU：
zh_nlp = stanza.Pipeline('zh', use_gpu=False)
text = "马云在1998年7月31日出生于江苏省盐城市大丰区。"

doc = zh_nlp(text)
for sent in doc.sentences:
    print("Sentence：" + sent.text)  # 断句
    print("Tokenize：" + ' '.join(token.text for token in sent.tokens))  # 中文分词
    print("UPOS: " + ' '.join(f'{word.text}/{word.upos}' for word in sent.words))  # 词性标注（UPOS）
    print("XPOS: " + ' '.join(f'{word.text}/{word.xpos}' for word in sent.words))  # 词性标注（XPOS）
    print("NER: " + ' '.join(f'{ent.text}/{ent.type}' for ent in sent.ents))  # 命名实体识别
