# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.conf import settings
import pymongo
import datetime


class SpiderChina10Pipeline(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)

    def process_item(self, item, spider):
        i = item['update_item']
        second_names = i['second_names']
        second_urls = i['second_urls']

        for second_name, second_url in zip(second_names, second_urls):
            try:
                spider.mongo_db.content_test_j1.insert_one(
                    {
                        'first_name': i['first_name'],
                        'first_url': i['first_url'],
                        'second_name': second_name,
                        'second_url': second_url
                    })

                spider.log('insert mongo succed!  second_name=%s, second_url=%s ' % (second_name, second_url), level=log.INFO)
            except pymongo.errors.DuplicateKeyError:
                spider.log('insert url is existed! ' , level=log.WARNING)
                continue
            except Exception, e:
                spider.log('insert mongo failed! (%s)' % (str(e)), level=log.ERROR)
