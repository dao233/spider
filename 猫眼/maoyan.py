import requests
import json


headers = {
'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; MI 6  Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 TitansX/11.14.7 KNB/1.2.0 android/5.1.1 com.sankuai.moviepro/com.sankuai.moviepro/5.4.4 App/10a20/5.4.4 com.sankuai.moviepro/5.4.4',
}

def get_one(offset):
	url = 'https://m.maoyan.com/review/v2/comments.json?'
	params = {
		'movieId': '1211727',
		'userId': '-1',	
		'offset': offset,  #offset控制传来第几页数据
		'limit': '15',
		'ts': '0',
		'type': '3',
	}
	r = requests.get(url=url,params=params,verify=False)  #verify=False为避免ssl认证,防止访问https时报错,这里假设所有访问都会正常，没有加容错机制。
	js = json.loads(r.text)  #将返回的json转为字典类型
	with open('fantan4.json','a',encoding='utf-8') as f:
		json.dump({"items":js['data']['comments']}, f, ensure_ascii=False, sort_keys=True, indent=4)  #写获取的所有详情到json文件中
		f.write(',')  #这里加一个','是为了之后将json文件格式改造正确所用
	comments = []
	for dic in js['data']['comments']:
		comments.append(dic['content'])  #这里获取每条影评到列表
	str1 = ' '.join(comments)  #影评列表转字符串以' '分开
	print(str1)
	with open('com.txt','a',encoding='utf-8') as f:
		f.write(str1)  #单独写入影评到文件，用于词云的生成
for i in range(0,67):
	print(i)
	get_one(i*15)
