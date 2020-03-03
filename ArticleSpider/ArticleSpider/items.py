# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
from scrapy.loader import ItemLoader  #用来重载这个类
from w3lib.html import remove_tags

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class QuestionItem(scrapy.Item):
    '''
    问题的item,问题和答案分两个集合保存在mongodb中
    '''

    title = scrapy.Field()
    created = scrapy.Field()
    answer_num = scrapy.Field()
    comment_num = scrapy.Field()
    follow_nums = scrapy.Field()
    question_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    author_url = scrapy.Field()
    author_name = scrapy.Field()
    author_headline = scrapy.Field()
    author_gender = scrapy.Field()
    crawl_time = scrapy.Field()


class Answer_Item(scrapy.Item):
    '''
    答案的item
    '''
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comment_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
