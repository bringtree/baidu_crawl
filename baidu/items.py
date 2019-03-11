# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    """
    关键字 item模型
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    search_key = scrapy.Field()
    question = scrapy.Field()
    href = scrapy.Field()

class QuestionAnswerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    问题-答案 模型
    """
    question = scrapy.Field()
    question_href = scrapy.Field()

    answer_1 = scrapy.Field()
    answer_1_author = scrapy.Field()
    answer_1_like = scrapy.Field()
    answer_1_unlike = scrapy.Field()

    answer_2 = scrapy.Field()
    answer_2_author = scrapy.Field()
    answer_2_like = scrapy.Field()
    answer_2_unlike = scrapy.Field()

    answer_3 = scrapy.Field()
    answer_3_author = scrapy.Field()
    answer_3_like = scrapy.Field()
    answer_3_unlike = scrapy.Field()

class SimilarityQuestionItem(scrapy.Item):
    """
    当前页面 和 相似问题模型
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    cur_page = scrapy.Field()
    first_question = scrapy.Field()
    first_href = scrapy.Field()

    second_question = scrapy.Field()
    second_href = scrapy.Field()
    second_rank = scrapy.Field()

