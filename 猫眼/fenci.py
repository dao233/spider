from os import path     #组织文件路径
from PIL import Image   #处理传入的背景图
#词云生成模块
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import jieba     #中文分词
import numpy as np
#中文处理
import matplotlib.font_manager as fm
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
#背景图
bg = np.array(Image.open('1.jpg'))

#获取当前项目路径
dir = path.dirname(__file__)

#添加自定义的分词
jieba.add_word('古天乐')
jieba.add_word('林峰')
jieba.add_word('反贪')
#一些词要去除，停用词表
stopwords_path='stopwords.txt'

#文本的名称
text_path='com.txt'

#读取要分析的文本
text = open(path.join(dir,text_path),encoding='utf-8').read()

#函数，用于分词
def jiebaClearText(text):
    #空列表，将已经去除的停用词的分词保存
    myWordList = []
    #分词
    seg_list = jieba.cut(text,cut_all=False)
    #seg_list类型是generator
    #将每个generator的内容用/连接
    listStr = '/'.join(seg_list)
    #停用表
    f_stop = open(stopwords_path,encoding='utf-8')
    #读取
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    #停用词格式化，用\n分开(因为原来文件里一行一个停用词),返回一列表

    f_stop_seg_list = f_stop_text.split('\n')
    #将用'/'结合的内容分开并去重用于去掉停用词

    bookList=listStr.split('/')

    #默认模式遍历，去掉停用词
    for myword in bookList :
        #去掉停用词，逻辑：若内容不在停用词列表且长度>1则收录
        if not ((myword.split())) in f_stop_seg_list and len(myword.strip())>1:
            myWordList.append(myword)
    return myWordList
text1 = jiebaClearText(text)

#计算词频
frequency = {}
for i in text1:
    print(i)
    if i in frequency:
        frequency[i]+=1
    else:
        frequency[i]=1

print(frequency)
#生成
wc = WordCloud(
    background_color = 'white',   #背景色
    max_words = 300,  #最大显示词数
    mask = bg,    #图片背景
    min_font_size=6,  # 字最大尺寸
    max_font_size = 100,   #字最大尺寸
    random_state = 42,
    font_path='C:/Windows/Fonts/simkai.ttf' #字体
).fit_words(frequency)

#为图片设置字体
my_font = fm.FontProperties(fname='C:/Windows/Fonts/simkai.ttf')

#产生背景图片，基于彩色图像的颜色生成器
image_colors = ImageColorGenerator(bg)
#画图
plt.imshow(wc.recolor(color_func=image_colors))

#为云图去掉坐标轴
plt.axis('off')
#画云图，显示
plt.figure()
#为背景图去掉坐标轴
plt.axis('off')
plt.imshow(bg,cmap=plt.cm.gray)

#保存
wc.to_file('man.png')
