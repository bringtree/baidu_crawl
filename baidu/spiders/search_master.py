# -*- coding: utf-8 -*-

from baidu.scrapy_redis_bloomfilter.RedisCrawlSpider_for_search import RedisCrawlSpider as RedisCrawlSpider
from baidu.items import BaiduItem
import re


class SearchMasterSpider(RedisCrawlSpider):
    name = 'search_master_spider'
    allowed_domains = ['baidu.com']
    redis_key = 'search:start_urls'

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
