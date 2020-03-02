# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self, databaseIp='127.0.0.1', databasePort=27017, user="", password="", ):
        self.client = MongoClient(databaseIp, databasePort)
        # self.db = self.client.test_database
        # self.db.authenticate(user, password)

    def process_item(self, item, spider):

        item = dict(item)  # 把item转化成字典形式
        print(item)
        mongodbName = 'news'
        self.db = self.client[mongodbName]
        # 更新插入问题数据
        self.db.sciencenews.update({'url': item['url']}, {'$set': item}, upsert=True)
        return item
