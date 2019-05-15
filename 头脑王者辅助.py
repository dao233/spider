import os
import random
import requests
import subprocess

from PIL import Image
from aip import AipOcr
from io import BytesIO


config={
    '头脑王者':{
        'title':(200,420,890,790), #用来记录标题的位置
        'answers':(80,960,1000,1720),
        'point':[
            (316,993,723,1078),
            (316,1174,723,1292),
            (316,1366,723,1469),
            (316,1570,723,1657),#四个答案的位置
        ]
    }
}

def get_screenshot():
    process=subprocess.Popen('adb shell screencap -p',shell=True,stdout=subprocess.PIPE)
    #相对于在cmd下执行了adb shell screencap -p，将会去截手机屏幕图
    screenshot=process.stdout.read()
    #读取截到的数据

    screenshot=screenshot.replace(b'\r\n', b'\n')
    #adb直接截的图在有点的问题，以二进制替换一下字符就可以了。
    img_fb=BytesIO()
    #BytesIO操作二进制数据，因为图片是二进制文件
    img_fb.write(screenshot)
    #写入内存
    img=Image.open(img_fb)
    #在内存打开图片
    title_img=img.crop((200,420,890,790))
    #对应(left, upper, right, lower)剪出来的是问题那部分图片
    answers_img=img.crop((80,960,1000,1720))
    #剪出来的是答案那部分图片

    new_img=Image.new('RGBA',(920,1140))
    #新建一张图片，用来保存上面剪问题和答案部分，就是去掉了玩家头像之类的那些杂质
    new_img.paste(title_img,(0,0,690,370))
    #问题部分粘贴新的大图
    new_img.paste(answers_img,(0,380,920,1140))
    #答案部分粘贴新的大图，过滤了不必要的元素

    new_img_fb=BytesIO()
    new_img.save(new_img_fb,'png')
    #保存图片
    with open('test.png','wb') as f:
        f.write(new_img_fb.getvalue())
    return new_img_fb  #返回新生成的图片
def get_word_by_image(img):
    APPID = '11788835'
    APIKey = 'tzZW1S0Ug3A5WhHCQP9RK9jT'
    SecretKey = 'TS9BAF7dIp4F7yDbVTd0qMXCUS6EjEB4'  #这三个都在账号里面
    client = AipOcr(APPID, APIKey, SecretKey)  #创建链接
    res=client.basicGeneral(img)  #将图片传过去
    return res  #识图结果
def baidu(question,answer):
    url='https://www.baidu.com/s'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    data={
        'wd':question
    }
    res=requests.get(url=url,params=data,headers=headers)
    res.encoding=res.apparent_encoding
    html=res.text
    for i in range(len(answer)):
        answer[i]=(html.count(answer[i]),answer[i],i)  #循环4次，将答案在百度返回源码中出现的次数统计出来
    answer.sort(reverse=True)  #按降序排序答案，以出现在源码中次数最高的为答案
    return answer


def click(point):
    cmd='adb shell input swipe %s %s %s %s %s'%(
        point[0],
        point[1],
        point[0]+random.randint(0,3),  #swipe实际上是拖动手机，这里加randint（0,3）是为了模拟长按手机
        point[1]+random.randint(0,3),
        200  #上面4个为坐标，这个200为持续点击的时间ms为它的单位
    )
    os.system(cmd)
def run():
    print('准备答题')
    while True:
        input('请按回车键开始答题：')
        img=get_screenshot()
        info=get_word_by_image(img.getvalue())
        if info['words_result_num']<5:
            continue
        answers=[x['words'] for x in info['words_result'][-4:]]  #提取返回的对应题目答案的中文字符串，这个与百度云返回的数据结构有关，不必深究，会用就行
        question=''.join([x['words'] for x in info['words_result'][:-4]])  #提取返回的问题的中文字符串
        res=baidu(question,answers)
        print(question)
        print(res)
        print(config['头脑王者']['point'][res[0][2]])
        click(config['头脑王者']['point'][res[0][2]])  #模拟点击
if __name__=='__main__':
    run()


