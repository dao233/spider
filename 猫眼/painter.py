from pyecharts import Bar
import json


#用于记录不同性别的打分
all = {0:[0,0,0,],1:[0,0,0,],2:[0,0,0,],3:[0,0,0,],4:[0,0,0,],5:[0,0,0,],6:[0,0,0,],7:[0,0,0,],8:[0,0,0,],9:[0,0,0,],10:[0,0,0,]}
with open('fantan4.json','r',encoding='utf-8') as f:
	js = json.loads(f.read())

for i in js['all']:
	items = i['items']
	for details in items:
		score = details['score']
		#取分数
		gender = details['gender']
		#取对应性别
		all[score][gender]+=1
		print(all)
male,female,none = zip(all[0],all[1],all[2],all[3],all[4],all[5],all[6],all[7],all[8],all[9],all[10])
#以性别分开数据，这么做为了将数据转化满足pyecharts输入的要求

attr = ['0分','1分','2分','3分','4分','5分','6分','7分','8分','9分','10分']
#0为男，1为女，2为未知
bar = Bar("评分",)
bar.add("男性评分", attr, male, is_stack=True)
bar.add("女性评分", attr, female, is_stack=True)
bar.add("未知性别评分", attr, none, is_stack=True)
bar.render('1.html')