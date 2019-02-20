# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    search_key = scrapy.Field()
    question = scrapy.Field()
    href = scrapy.Field()


class SimilarityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    faq_question = scrapy.Field()
    similarity_question = scrapy.Field()
    href = scrapy.Field()
    like = scrapy.Field()
