# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    type_ = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    city = scrapy.Field()
