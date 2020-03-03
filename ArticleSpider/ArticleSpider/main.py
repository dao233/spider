from scrapy.cmdline import execute
import sys
import os


# os.path.abspath(__file__)当前py文件的路径
# os.path.dirname(os.path.abspath(__file__))当前文件目录
# 设置工程目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 相当于在cmd里执行scrapy crawl zhihu
execute(['scrapy','crawl','zhihu'])
