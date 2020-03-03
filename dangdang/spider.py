import requests
import json
import random
import time


url='http://api.dangdang.com/community/mobile/get_product_comment_list?access-token=&product_id=25288851&time_code=ae4074539cd0bf4ad526785a9439d756&tc=0cdfe66abc1ef55674c1ca8f815414b0&client_version=8.10.0&source_page=&action=get_product_comment_list&ct=android&union_id=537-100893&timestamp=1540121525&permanent_id=20181021192526739954846678302543739&custSize=b&global_province_id=111&cv=8.10.0&sort_type=1&product_medium=0&page_size=15&filter_type=1&udid=c3b0e748134cbd9612e3e8b6a7e52952&main_product_id=&user_client=android&label_id=&page='
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
def getComments(url, page):
    url = url+str(page)  #url拼接，为了获取指定页的评论
    html = requests.get(url=url,headers=headers)
    res = json.loads(html.text)
    result = res.get('review_list')  #从字典中获取key为review_list的值，这与当当返回的数据结构有关
    comments = []
    for comment in result:
        comments.append(comment['content'])  #评论正文
        try:
            with open('comments.txt','a',encoding='utf-8') as f:
                f.write(comment['content']+'\n')  #写入文本中，免不了编码错误，加个try算了
        except:
            print('第'+str(page)+'页出错')
            continue
for i in range(1,100):  #爬100页的评论
    time.sleep(random.choice([1,2,3]))  #每次循环强制停1~3秒，控制下频率...
    getComments(url,i)