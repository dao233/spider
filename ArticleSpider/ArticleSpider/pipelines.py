# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from pymongo import MongoClient

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self, databaseIp='', databasePort=27017, username="", password="",):
        self.client = MongoClient(host=databaseIp, port=27017, username=username, password=password)

    def process_item(self, item, spider):

        postItem = dict(item)  # 把item转化成字典形式
        print(postItem)
        if item.__class__.__name__ == 'QuestionItem':
            mongodbName = 'zhihu'
            self.db = self.client[mongodbName]
            # 更新插入问题数据
            self.db.question.update({'question_id':postItem['question_id']},{'$set':postItem},upsert=True)
            
        elif item.__class__.__name__ == 'Answer_Item':
            mongodbName = 'zhihu'
            self.db = self.client[mongodbName]
            # 更新插入答案数据
            self.db.answer.update({'answer_id': postItem['answer_id']}, {'$set': postItem}, upsert=True)
        # 会在控制台输出原item数据，可以选择不写
        return item
    def close_spider(self, spider):
        self.client.close()

