# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import  ItemLoader
from scrapy.loader.processors import  TakeFirst, Compose, Join
from scrapyuniversal.items import NewsItem
import time


#scrapy crawl sciencenews
class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()
    abstract_out = Compose(Join(), lambda x: x.strip())
    tag_out = Compose(Join(), lambda x:x.strip())
    author_desc_out = Compose(Join(), lambda x:x.strip())


class SciencenewsSpider(CrawlSpider):
    name = 'sciencenews'
    allowed_domains = ['www.sciencenews.org']
    start_urls = ['https://www.sciencenews.org/all-stories/page/2']

    rules = (
        Rule(LinkExtractor(allow=r'article/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next page-numbers"]'), follow=True),
    )

    def parse_item(self, response):
        loader = NewsLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//h1[contains(@class,"header-default__title")]/text()')
        loader.add_xpath('abstract', '//h2[contains(@class,"header-default__deck")]/text()')
        loader.add_xpath('author', '//span[@class="byline author vcard"]//a/text()')
        loader.add_xpath('author_url', '//span[@class="byline author vcard"]//a/@href')
        loader.add_xpath('author_desc', '//div[contains(@class,"author-bio__bio")]/p//text()')
        loader.add_xpath('publish_time', '//time[contains(@class,"byline__published")]/@datetime')
        loader.add_xpath('content', '//div[contains(@class,"rich-text")]')
        loader.add_xpath('tag', '//span[contains(@class,"header-default__eyebrow")]/a/text()')
        loader.add_value('crawl_time', int(time.time()))
        loader.add_value('url', response.url)
        return loader.load_item()
