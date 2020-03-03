import jieba
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.globals import SymbolType


#添加自定义的分词
jieba.add_word('你坏')
jieba.add_word('大冰')
jieba.add_word('江湖')

#文本的名称
text_path='comments.txt'
#一些词要去除，停用词表
stopwords_path='stopwords.txt'

#读取要分析的文本
words_file = open(text_path,'r',encoding='utf-8')
text = words_file.read()


def jiebaClearText(text):

    #分词，返回迭代器
    seg_iter = jieba.cut(text,cut_all=False)
    listStr = list(seg_iter)

    res = {}
    #这个循环用来记录词频
    for i in listStr:
        if i in res:
            res[i] += 1
        else:
            res[i.strip()] = 1
    try:
        #读取停用表
        f_stop = open(stopwords_path,encoding='utf-8')
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    #以换行符分开文本,因为每个停用词占一行。返回停用词列表
    f_stop_seg_list = f_stop_text.split('\n')
    #这个循环用来删除评论出现在停用词表的词
    for i in f_stop_seg_list:
        if i in res:
            del res[i]

    words = []
    for k,v in res.items():
        words.append((k,v))
    #words的元素是(词，词出现的次数)
    #下面是以出现的次数将words排序
    words.sort(key=lambda x:x[1],reverse=True)
    return words

words = jiebaClearText(text)
words_file.close()  # 关闭一开始打开的文件
print(words)
#词云生成，用到pyecharts，各参数的含义请到官方文档查看...
worldcloud=(
    WordCloud().add("", words[:60], word_size_range=[10, 100],rotate_step=0, shape='triangle' ).set_global_opts(title_opts=opts.TitleOpts(title="《你坏》"))
    )
worldcloud.render('result.html')  #保存成html文件


