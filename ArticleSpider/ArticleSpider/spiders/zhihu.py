# -*- coding: utf-8 -*-
import re
import time
import json
import datetime
import scrapy

from ArticleSpider.items import QuestionItem, Answer_Item
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider


def timestamp_2_date(timestamp):
    '''
    用来将时间戳转为日期时间形式
    '''
    time_array = time.localtime(timestamp)
    my_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return my_time

class ZhihuSpider(RedisSpider):
    # spider名
    name = 'zhihu'
    # 允许访问的域名
    allowed_domains = ['www.zhihu.com']
    # redis_key，到时scrapy会去redis读这个键的值，即要访问的url,原来start_url的值也是放在redis里
    redis_key = 'zhihu:start_urls'
    # spider的设置，在这里设置可以覆盖setting.py里的设置
    custom_settings = {
        # 用来设置随机延迟，最大5秒
        "RANDOM_DELAY": 5,
        'ITEM_PIPELINES':{
            # 如果要使用scrapy-redis, RedisPipeline必须设置，
            'scrapy_redis.pipelines.RedisPipeline': 3,
            # MongoPipeline则是用来保存爬取的数据的。
            'ArticleSpider.pipelines.MongoPipeline': 4,
        },
    }
    # 上面这样设置好了就能使用scrapy-redis进行分布式的爬取，其他的比如parse()函数按照scrapy的逻辑设置就好
    # 答案的api
    answer_api = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&platform=desktop&sort_by=default'

    def parse(self, response):
        '''
        解析首页，获取所有url，实现深度优先的爬取
        '''
        # 每次请求知乎问题api都会返回一个新的set-cookie(只是一段cookie)，用来设置新的cookie。旧的cookie无法访问下一页的链接
        cookie_section = response.headers.get('set-cookie')
        # 匹配cookie片段
        sections  = re.findall('(KLBRSID=.*?);', str(cookie_section))
        print(sections)
        raw_cookie = response.request.headers['Cookie'].decode('utf-8')
        # 替换cookie片段到完整cookie里
        cookie = re.sub('KLBRSID=.*', sections[0], raw_cookie)
        print(cookie)
        # 请求首页后，在首页html源码里寻找问题的api
        question_api = re.findall('"previous":"(.*?)","next', response.text, re.S)
        question_url = question_api[0].replace('\\u002F', '/')
        # 用新的cookie请求问题api,回调函数为parse_question
        yield Request(url=question_url,callback=self.parse_question,headers={'cookie':cookie})

    def parse_question(self,response):
        '''
        解析问题api返回的json数据
        '''
        # 构造新cookie
        cookie_section = response.headers.get('set-cookie')
        sections  = re.findall('(KLBRSID=.*?);', str(cookie_section))
        print(sections)
        raw_cookie = response.request.headers['Cookie'].decode('utf-8')
        cookie = re.sub('KLBRSID=.*', sections[0], raw_cookie)
        dics = json.loads(response.text)
        for dic in dics['data']:
            try:
                ques_item = QuestionItem()
                if 'question' in dic['target']:
                    # 问题标题
                    ques_item['title'] = dic['target']['question']['title']
                    # 问题创建时间
                    ques_item['created'] = dic['target']['question']['created']
                    ques_item['created'] = timestamp_2_date(ques_item['created'])
                    # 回答数
                    ques_item['answer_num'] = dic['target']['question']['answer_count']
                    # 评论数
                    ques_item['comment_num'] = dic['target']['question']['comment_count']
                    # 关注人数
                    ques_item['follow_nums'] = dic['target']['question']['follower_count']
                    # 问题id
                    ques_item['question_id'] = dic['target']['question']['id']
                    #问题url
                    ques_item['url'] = dic['target']['question']['id']
                    ques_item['url'] = 'https://www.zhihu.com/question/' + str(ques_item['url'])
                    # 问题标签
                    if 'uninterest_reasons' in dic:
                        topics = []
                        for i in dic['uninterest_reasons']:
                            topics.append(i['reason_text'])
                    ques_item['topics'] = topics
                    # 作者url
                    ques_item['author_url'] = dic['target']['question']['author']['url']
                    # 作者名
                    ques_item['author_name'] = dic['target']['question']['author']['name']
                    # 作者签名
                    ques_item['author_headline'] = dic['target']['question']['author']['headline']
                    # 作者性别
                    ques_item['author_gender'] = dic['target']['question']['author'].get('gender')
                    if ques_item['author_gender']:
                        if ques_item['author_gender'] == 0:
                            ques_item['author_gender'] = '女'
                        else:
                            ques_item['author_gender'] = '男'
                    else:
                        ques_item['author_gender'] = '未知'
                    # 爬取时间
                    ques_item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    yield ques_item
            except:
                pass
        # 问题api里会有个is_end的值，用来判断是否还有下一页
        if not dics['paging']['is_end']:
            # 有下一页，获取next里的下一页链接
            next_url = dics['paging']['next']
            # 用新的cookie请求下一页问题url
            yield Request(url=next_url, callback=self.parse_question, headers={'cookie': cookie})
            # 请求答案api，api需要传入question_id, limit及页码
            yield Request(url=self.answer_api.format(ques_item['question_id'], 20, 0), callback=self.parse_answer)

    def parse_answer(self,response):
        #处理answerAPI返回的json
        ans_json = json.loads(response.text)
        # is_end的值意味着当前url是否是最后一页
        is_end = ans_json['paging']['is_end']
        totals_answer = ans_json['paging']['totals']
        # 下一页url
        next_url = ans_json['paging']['next']
        for answer in ans_json['data']:
            ans_item = Answer_Item()
            # 答案id
            ans_item['answer_id'] = answer['id']
            # 答案对应的问题id
            ans_item['question_id'] = answer['question']['id']
            # 答案url
            ans_item['url'] = answer['url']
            # 答者用户名
            ans_item['user_name'] = answer['author']['name'] if 'name' in answer['author'] else None
            # 答者id
            ans_item['user_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            # 答案内容
            ans_item['content'] = answer['content'] if 'content' in answer else None
            # 赞同人数
            ans_item['praise_num'] = answer['voteup_count']
            # 评论人数
            ans_item['comment_num'] = answer['comment_count']
            # 答案创建时间
            ans_item['create_time'] = answer['created_time']
            ans_item['create_time'] = timestamp_2_date(ans_item['create_time'])
            # 答案修改时间
            ans_item['update_time'] = answer['updated_time']
            ans_item['update_time'] = timestamp_2_date(ans_item['update_time'])
            # 爬取时间
            ans_item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield ans_item
        # offset偏移，一页20，每问题只爬50页评论。即offest>1000
        offset = next_url.split('offset=')[1].split('\u0026')[0]
        if int(offset)>1000:
            pass
        else:
            if not is_end:
                yield scrapy.Request(url=next_url, callback=self.parse_answer)



