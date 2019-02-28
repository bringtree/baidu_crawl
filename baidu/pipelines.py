# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import pymysql.cursors
import twisted.enterprise.adbapi as adbapi
import logging
from select_pipelines import check_spider_pipeline

logger = logging.getLogger('bd')


class BaiduPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def open_spider(self, spider):
        pass

    @check_spider_pipeline(['bd', 'search_master_spider'])
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def close_spider(self, spider):
        self.dbpool.close()

    @classmethod
    def from_settings(cls, crawler):
        dbparams = dict(
            host=crawler['MYSQL_HOST'],
            port=crawler['MYSQL_PORT'],
            db=crawler['MYSQL_DBNAME'],
            user=crawler['MYSQL_USER'],
            passwd=crawler['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def _conditional_insert(self, tx, item):
        sql = "insert into key_question(search_key,question,href) values(%s,%s,%s);"
        params = (item['search_key'], item['question'], item['href'])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        # TODO 异常处理的代码还没有写完!
        if 'Duplicate entry' in failue.value.args[1]:
            logger.info('重复了')
        else:
            logger.error(failue)


class SimilarityPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def open_spider(self, spider):
        pass

    @check_spider_pipeline(['similarity_question'])
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def close_spider(self, spider):
        self.dbpool.close()

    @classmethod
    def from_settings(cls, crawler):
        dbparams = dict(
            host=crawler['MYSQL_HOST'],
            port=crawler['MYSQL_PORT'],
            db=crawler['MYSQL_DBNAME'],
            user=crawler['MYSQL_USER'],
            passwd=crawler['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def _conditional_insert(self, tx, item):
        # TODO 这个2记得要改
        if item['cur_page'] < 3:
            sql = "insert into question_answer(question,question_href," \
                  "answer_1,answer_1_author,answer_1_like,answer_1_unlike," \
                  "answer_2,answer_2_author,answer_2_like,answer_2_unlike," \
                  "answer_3,answer_3_author,answer_3_like,answer_3_unlike) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            params = (item['first_question'], item['question_href'],
                      item['answer_1'],item['answer_1_author'],item['answer_1_like'],item['answer_1_unlike'],
                      item['answer_2'],item['answer_2_author'],item['answer_2_like'],item['answer_2_unlike'],
                      item['answer_3'],item['answer_3_author'],item['answer_3_like'],item['answer_3_unlike'],)
            tx.execute(sql, params)

            sql = "insert into similarity_question(first_question,second_question,first_href,second_href,second_rank) values(%s,%s,%s,%s,%s);"
            params = (item['first_question'], item['second_question'], 'https://zhidao.baidu.com' + item['first_href'],
                      'https://zhidao.baidu.com' + item['second_href'], item['second_rank'])
            tx.execute(sql, params)
        else:
            sql = "insert into question_answer(question,question_href," \
                  "answer_1,answer_1_author,answer_1_like,answer_1_unlike," \
                  "answer_2,answer_2_author,answer_2_like,answer_2_unlike," \
                  "answer_3,answer_3_author,answer_3_like,answer_3_unlike) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            params = (item['first_question'], item['question_href'],
                      item['answer_1'], item['answer_1_author'], item['answer_1_like'], item['answer_1_unlike'],
                      item['answer_2'], item['answer_2_author'], item['answer_2_like'], item['answer_2_unlike'],
                      item['answer_3'], item['answer_3_author'], item['answer_3_like'], item['answer_3_unlike'],)
            tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        # TODO 异常处理的代码还没有写完!
        if 'Duplicate entry' in failue.value.args[1]:
            logger.info('重复了')
        else:
            logger.error(failue)
