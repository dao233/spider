#encoding:utf-8
import random
from pyecharts import Bar
from pymongo import MongoClient


conn = MongoClient('127.0.0.1',27017)  #创建于MongoDB的连接
db = conn.anjuke  #选择数据库
collection=db.AnjukeItem  #选择数据库下的集合
all = []
res = collection.aggregate([
        {'$group':{'_id':'$city',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},])
conn.close()
#上面是mongodb聚合统计的语句
#$group：按照给定表达式组合结果，这里的_id字段表示你要基于哪个字段来进行分组，这里的$city就表示要基于city字段来进行分组
#下面的count字段的值$sum: 1表示的是获取--满足city字段相同的这一组的数量--乘以后面给定的值(本例为1，那么就是同组的数量)。
#$sort：按照给定的字段排序结果，即按计算好的count排序，-1为降序来排列

for i in res:
    print(i)
    #{'_id': '成都', 'count': 2074}
    all.append((i['_id'].strip(),i['count']))

attr = [i[0] for i in all[:30] ]  #取前三十城市的名字
v1 = [i[1] for i in all[:30]]  #取前三十城市的值
print(attr)
bar = Bar('新房分布柱状图')  #柱状图
bar.add('各城市新楼盘数',attr,v1,is_label_show=True,is_datazoom_show=True,xaxis_rotate=65, label_color=['#87CEEB',])
#attr  下面的城市名
#v1  数值
#is_label_show -> bool  是否正常显示标签，默认不显示。即各柱上的数字
#is_datazoom_show -> bool  是否使用区域缩放组件，默认为 False
#xaxis_rotate -> int  x 轴刻度标签旋转的角度，默认为 0，即不旋转。旋转的角度从 -90 度到 90 度。
#label_color  柱的颜色
bar.render('bar.html')
