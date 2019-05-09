#encoding:utf-8
from pymongo import MongoClient
from pyecharts import Bar


conn = MongoClient('127.0.0.1',27017)
db = conn.anjuke
collection=db.AnjukeItem
res = collection.find()
conn.close()
#连接mongodb的逻辑，同上~

all = {}
for i in res:
    city = i['city']  #获取城市名
    try:

        if i['price'][1].isdecimal():  #判断i['price'][1]是不是数字型的价格
            price_type = i['price'][0]  #获取价格类型
            price = i['price'][1]
            price = int(price)  #str价格转int价格
        elif i['price'][2].isdecimal():  #判断i['price'][2]是不是数字型的价格
            price_type = i['price'][1]  #获取价格类型
            price = i['price'][2]
            price = int(price)  #str价格转int价格
    except:
        continue


    if '均价' in price_type:  #只取均价
        if city in all:
            all[city].append(price)
        else:
            all[city] = [price,]
print(all)
#{'_id': '黑河', 'count': 17}
#{'_id': '甘南', 'count': 17}
#{'_id': '陇南', 'count': 16}
all_avg = []
for city,prices in all.items():
    all_avg.append((city,sum(prices)/len(prices)))  #计算所有的城市房价平均值，all_avg里的元素为元组（城市名,均价）
all_avg = sorted(all_avg,key=lambda x:x[1],reverse=True)  #降序排序

print(all_avg)
#[('深圳', 59192.21692307692), ('上海', 50811.7504091653), ...



attr = [i[0] for i in all_avg[:30] ]  #获取前30城市名
v1 = ['{:.1f}'.format(i[1]) for i in all_avg[:30]]  #获取前30名的值
bar = Bar('各城市房价平均值')
bar.add('单位面积价格（元/平米）',attr,v1,is_label_show=True,is_datazoom_show=True)
#画图逻辑，同上
bar.render('bar2.html')
