# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    abstract= Field()
    url = Field()
    author = Field()
    author_url = Field()
    author_desc = Field()
    publish_time = Field()
    content = Field()
    tag = Field()
    crawl_time = Field()
