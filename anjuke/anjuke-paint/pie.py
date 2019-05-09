from pyecharts import Pie
from pymongo import MongoClient

conn = MongoClient('127.0.0.1',27017)
db = conn.anjuke
collection=db.AnjukeItem
#Mongodb的连接
all = []
res = collection.aggregate(
    [
    {
        '$unwind': '$type_'
    },{
        '$group': {
            '_id': '$type_',
            'count': {'$sum': 1}
        }
    }
    ]
)
#上面是mongodb聚合统计的语句
#'$unwind': '$type_'因为type_是一个列表这里是将type_拆分了，用以下面的计算
#$group：按照给定表达式组合结果，这里的_id字段表示你要基于哪个字段来进行分组，这里的$type_就表示要基于type_字段来进行分组
#下面的count字段的值$sum: 1表示的是获取--满足type_字段相同的这一组的数量--乘以后面给定的值(本例为1，那么就是同组的数量)。
conn.close()

all = []
for i in res:
    print(i)
    #{'_id': '商业', 'count': 337}
    #{'_id': '商办', 'count': 158}
    #{'_id': '8室', 'count': 76}
    if '室' in i['_id']:  #只取有'室'关键字的数据
        all.append((i['_id'],i['count']))
all = sorted(all,key=lambda x:x[1],reverse=True)  #以数量进行排序
print(all)


attr = [i[0] for i in all][:6]  #取前六的类型名
v1 = [i[1] for i in all][:6]  #取前六的数值

pie =Pie("户型比例", title_pos='center', width=900)
#pie.add("商品A", attr, v1, center=[25, 50], is_random=True, radius=[30, 75], rosetype='radius')
pie.add("商品B", attr, v1, is_random=True, radius=[30, 75], rosetype='area', is_legend_show=False, is_label_show=True)
#is_random为是否随即排列颜色列表
#radius为半径，第一个为内半径，第二个是外半径；
#rosetype为是否展示成南丁格尔图（ 'radius' 圆心角展现数据半分比，半径展现数据大小；'area' 圆心角相同，为通过半径展现数据大小）
#is_label_show为是否显示标签（各个属性的数据信息）
#is_legend_show:是否显示图例
pie.render('pie.html')