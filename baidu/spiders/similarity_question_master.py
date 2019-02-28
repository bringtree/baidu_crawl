# -*- coding: utf-8 -*-
import scrapy
import re
from baidu.items import SimilarityItem
from baidu.spiders.RedisCrawlSpider_for_similarity import RedisCrawlSpider

pattern = r'(?<=)valueNum":[0-9]+,"valueBadNum\"\:[0-9]+'


class SimilarityQuestionSpider(RedisCrawlSpider):
    name = 'similarity_question'
    allowed_domains = ['zhidao.baidu.com']
    redis_key = 'similarity:start_urls'

    # start_urls = []
    def parse(self, response):
        cur_page = response.meta['cur_page']

        evaluate_value = re.findall(pattern, response.body.decode('ISO-8859-1'))
        good_bad = []
        for _ in evaluate_value:
            good_bad.append(re.findall(r"\d+", _))

        for rank_idx, similarity_css in enumerate(response.css('.related-link-zd')):
            item = SimilarityItem()
            item['cur_page'] = cur_page
            item['first_question'] = response.css('.ask-title::text').get()
            item['first_href'] = response.meta['first_href']
            item['second_question'] = similarity_css.css('.related-restrict-title ::text').get()
            item['second_href'] = re.search(r'/question/[\s\S]+.html',
                                            similarity_css.css('.related-link ::attr(href)').get()).group(0)

            item['second_rank'] = rank_idx + 1
            answer_list = response.css('.mb-10')
            item['question_href'] = response.meta['first_href']

            item['answer_1'] = ''
            item['answer_1_author'] = ''
            item['answer_1_like'] = ''
            item['answer_1_unlike'] = ''

            item['answer_2'] = ''
            item['answer_2_author'] = ''
            item['answer_2_like'] = ''
            item['answer_2_unlike'] = ''

            item['answer_3'] = ''
            item['answer_3_author'] = ''
            item['answer_3_like'] = ''
            item['answer_3_unlike'] = ''

            if len(answer_list) >= 1:
                item['answer_1'] = ''.join((answer_list[0]).xpath('text()').extract())
                item['answer_1_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[0]
                item['answer_1_like'] = good_bad[0][0]
                item['answer_1_unlike'] = good_bad[0][1]
            if len(answer_list) >= 2:
                item['answer_2'] = ''.join((answer_list[1]).xpath('text()').extract())
                item['answer_2_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[1]
                item['answer_2_like'] = good_bad[0][0]
                item['answer_2_unlike'] = good_bad[0][1]
            if len(answer_list) == 3:
                item['answer_3'] = ''.join((answer_list[2]).xpath('text()').extract())
                item['answer_3_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[2]
                item['answer_3_like'] = good_bad[0][0]
                item['answer_3_unlike'] = good_bad[0][1]

            yield item
            if cur_page + 1 <= 2:
                yield response.follow(item['second_href'], callback=self.parse, meta={
                    'first_href': item['second_href'],
                    'cur_page': cur_page + 1
                })
            if cur_page + 1 == 3:
                yield response.follow(item['second_href'], callback=self.parse, meta={
                    'first_href': item['second_href'],
                    'cur_page': cur_page + 1
                })
