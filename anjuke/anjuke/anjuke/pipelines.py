# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class TextPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):#类方法，用于从settins.py中获取在那边设置的MONGO_URI和MONGO_DB
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
            )
    def open_spider(self,spider):  #当spider开启时这个方法被调用，这里用来连接数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):  #实现了item数据插入到数据库，自动创建与项目名同名，spider同名的表，数据都保存在里面
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item
    def close_spider(self,spider):  #当spider关闭时这个方法被调用
        self.client.close()
