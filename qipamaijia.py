import aiohttp
import asyncio
import random
from lxml import etree

header = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
]
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
async def request(page):
    # 以async开始的函数返回的是一个协程
    headers['User-Agent'] = random.choice(header)
    url = 'http://www.qipamaijia.com/fuli/' + str(page)
    # with同打开文件时用的with一样作用
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            # 使用 await 可以将耗时等待的操作挂起,转而去执行别的协程，直到其他的协程挂起或执行完毕
            r = await resp.text()
            html = etree.HTML(r)
            imgs = html.xpath('//div[@class="block"]/div[@class="thumb"]//img/@src')
            for img_url in imgs:
                await down_img(img_url)


async def down_img(url):
    headers['User-Agent'] = random.choice(header)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            # 下面这种保存网络数据的方法是官方文档建议的
            filename = url.split('/')[-1]
            with open(filename, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(512)
                    if not chunk:
                        break
                    fd.write(chunk)
# 使用ensure_future创建task
tasks = [asyncio.ensure_future(request(_)) for _ in range(1,100)]
loop = asyncio.get_event_loop()
# 当run_until_complete的参数是task列表时，需加上asyncio.wait
loop.run_until_complete(asyncio.wait(tasks))