#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
from baidu.items import QuestionAnswerItem, SimilarityQuestionItem
from baidu.scrapy_redis_bloomfilter.RedisCrawlSpider_for_similarity import RedisCrawlSpider

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

        QAItem = QuestionAnswerItem()
        # 初始化问题-答案对象中的数据
        QAItem['question'] = response.css('.ask-title::text').get()
        QAItem['question_href'] = response.meta['first_href']
        QAItem['answer_1'] = ''
        QAItem['answer_1_author'] = ''
        QAItem['answer_1_like'] = 0
        QAItem['answer_1_unlike'] = 0

        QAItem['answer_2'] = ''
        QAItem['answer_2_author'] = ''
        QAItem['answer_2_like'] = 0
        QAItem['answer_2_unlike'] = 0

        QAItem['answer_3'] = ''
        QAItem['answer_3_author'] = ''
        QAItem['answer_3_like'] = 0
        QAItem['answer_3_unlike'] = 0

        # 提取答案列表
        answer_list = response.css('.mb-10')
        # 要去掉广告
        try:
            if ''.join((response.css('.mb-10')[0]).css('.guide-challenge li').xpath(
                'text()').extract()) == u'你的回答被采纳后将获得：系统奖励（财富值+成长值）+（财富值+成长值）':
                answer_list = answer_list[1:]
        except:
            answer_list = response.css('.mb-10')

        # 问答答案的数量不同，对应不同的处理方案
        if len(answer_list) >= 1:
            QAItem['answer_1'] = ''.join((answer_list[0]).xpath('text()').extract())
            QAItem['answer_1_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[0]
            QAItem['answer_1_like'] = good_bad[0][0]
            QAItem['answer_1_unlike'] = good_bad[0][1]
        if len(answer_list) >= 2:
            QAItem['answer_2'] = ''.join((answer_list[1]).xpath('text()').extract())
            QAItem['answer_2_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[1]
            QAItem['answer_2_like'] = good_bad[0][0]
            QAItem['answer_2_unlike'] = good_bad[0][1]
        if len(answer_list) == 3:
            QAItem['answer_3'] = ''.join((answer_list[2]).xpath('text()').extract())
            QAItem['answer_3_author'] = response.css('.wgt-replyer-all-uname  ::text').extract()[2]
            QAItem['answer_3_like'] = good_bad[0][0]
            QAItem['answer_3_unlike'] = good_bad[0][1]
        yield QAItem

        for rank_idx, similarity_css in enumerate(response.css('.related-link-zd')):
            # 相似问题模型对象
            SQitem = SimilarityQuestionItem()
            SQitem['cur_page'] = cur_page
            SQitem['first_question'] = response.css('.ask-title::text').get()
            SQitem['first_href'] = response.meta['first_href']
            SQitem['second_question'] = similarity_css.css('.related-restrict-title ::text').get()
            SQitem['second_href'] = re.search(r'/question/[\s\S]+.html',
                                              similarity_css.css('.related-link ::attr(href)').get()).group(0)

            SQitem['second_rank'] = rank_idx + 1

            yield SQitem

            # 控制当前页面深度为2，3是因为此时需要去看看3的相似问题答案所以才写3
            if cur_page + 1 <= 3:
                yield response.follow(SQitem['second_href'], callback=self.parse, meta={
                    'first_href': SQitem['second_href'],
                    'cur_page': cur_page + 1
                })
