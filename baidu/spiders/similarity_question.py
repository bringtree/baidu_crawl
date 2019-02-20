# -*- coding: utf-8 -*-
import scrapy
import re
from baidu.items import SimilarityItem


class SimilarityQuestionSpider(scrapy.Spider):
    name = 'similarity_question'
    allowed_domains = ['zhidao.baidu.com']

    # start_urls = []
    def start_requests(self):
        yield scrapy.Request('https://zhidao.baidu.com/question/2073937424040623828.html', callback=self.parse, meta={
            'depth': 1
        })

    def parse(self, response):
        cur_depth = response.meta['depth']
        for similarity_css in response.css('.related-link-zd'):
            item = SimilarityItem()
            item['faq_question'] = response.css('.ask-title::text').get()

            item['href'] = re.search(r'/question/[\s\S]+.html',
                                     similarity_css.css('.related-link ::attr(href)').get()).group(0)
            item['similarity_question'] = similarity_css.css('.related-restrict-title ::text').get()
            item['like'] = similarity_css.css('.ff-arial::text').get() or 0
            yield item
            if cur_depth + 1 < 5:
                yield response.follow(item['href'], callback=self.parse, meta={'depth': cur_depth + 1})
