#coding=utf-8
from pymongo import MongoClient
from pyecharts import Geo
import json

conn = MongoClient('127.0.0.1',27017)
db = conn.anjuke
collection=db.AnjukeItem
#res=collection.distinct("city")
all = []
res = collection.aggregate([
        {'$group':{'_id':'$city',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},])
for i in res:
    all.append((i['_id'].strip(),i['count']))
conn.close()
#连接查询，和图一一样


new_all =[]
with open('city_coordinates.json','r',encoding='utf-8') as f:
    #这里是复制到pyecharts的地理json数据和爬到的城市名对比，因为好多爬到的城市其实在pyecharts是没有记录的，直接绘图会报错
    #位置在\Python36\Lib\site-packages\pyecharts\datasets\city_coordinates.json
    all_city = json.loads(f.read(),encoding='utf-8')
for i in all:
    if i[0] in all_city:
        new_all.append(i)

geo = Geo(
    "全国新房分布",  #图标题
    "",  #副标题
    title_color="#fff",  #标题颜色
    title_pos="center",  #标题位置
    width=1200,  #图宽
    height=600,  #高
    background_color="#404a59",  #背景颜色
)
attr, value = geo.cast(new_all)  #分开城市名和数值


geo.add(
"",
attr,
value,
visual_range=[100, 1200],  #显示的数值范围
visual_text_color="#fff",  #鼠标放上去后显示的文字颜色
symbol_size=15,  #标记的大小
type='heatmap',  #类型为热力图
is_visualmap=True,
)

geo.render()