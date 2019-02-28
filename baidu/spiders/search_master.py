# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from baidu.spiders.RedisCrawlSpider_for_search import RedisCrawlSpider
import re

from baidu.items import BaiduItem
import re


class SearchMasterSpider(RedisCrawlSpider):
    name = 'search_master_spider'
    allowed_domains = ['baidu.com']
    redis_key = 'search:start_urls'

    #
    # custom_settings = {
    #     'REDIS_HOST': "0.0.0.0",
    #     'REDIS_PORT': "6380",
    #     'REDIS_PARAMS': {
    #         'password': '123456',
    #     }
    # }

    #
    # def __init__(self, *args, **kwargs):
    #     super(SearchMasterSpider, self).__init__(*args, **kwargs)
    #     self.page = 1
    #
    # def start_requests(self):
    #     with open('./keyword.txt') as fp:
    #         for keyword in fp.readlines():
    #             keyword = keyword.replace('\n', '')
    #             url = https://zhidao.baidu.com/search?ct=20&tn=ikaslist&word=%E4%B8%80&pn=0&rn=21
    #             yield scrapy.Request(url, self.parse, meta={'cur_page': 1, 'keyword': keyword})

    def parse(self, response):
        # 当前爬去页数
        keyword = response.meta['keyword']
        cur_page = response.meta['cur_page']

        for question in response.css('a.ti').getall():
            item = BaiduItem()
            item['search_key'] = keyword
            item['question'] = re.sub(r'<(?!<)[^<]*(?=>)>', '', question)
            item['href'] = re.search(r'http[s]?://[\s\S]+.html', question).group(0)
            yield item

        next_page = response.css('a.pager-next ::attr(href)').get()
        if next_page is not None and (cur_page + 1 <= 5):
            next_page += '&rn=21'
            yield response.follow(next_page, meta={'cur_page': cur_page + 1, 'keyword': keyword}, callback=self.parse)

        else:
            self.logger.info('key_word:' + keyword + ',爬取完毕')
