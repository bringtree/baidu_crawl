# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from baidu.items import BaiduItem
import re



class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['baidu.com']

    def start_requests(self):
        with open('./keyword.txt') as fp:
            for keyword in fp.readlines():
                keyword = keyword.replace('\n', '')
                url = 'http://zhidao.baidu.com/q?ct=17&tn=ikaslist&word=' + keyword + '&pn=0'
                yield scrapy.Request(url, self.parse, meta={'cur_page': 1, 'keyword': keyword})

    def parse(self, response):
        # 当前爬去页数
        cur_page = response.meta['cur_page']
        keyword = response.meta['keyword']

        for question in response.css('a.ti').getall():
            item = BaiduItem()
            item['search_key'] = keyword
            item['question'] = re.sub(r'<(?!<)[^<]*(?=>)>', '', question)
            try:
                item['href'] = re.search(r'http[s]?://[\s\S]+.html', question).group(0)
                yield item
            except AttributeError:
                print(1)

        next_page = response.css('a.pager-next ::attr(href)').get()
        if next_page is not None and (cur_page + 1 <= 5):
            yield response.follow(next_page, meta={'cur_page': cur_page + 1, 'keyword': keyword}, callback=self.parse)
        else:
            self.logger.info('key_word:' + keyword + ',爬取完毕')
