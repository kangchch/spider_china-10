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
        three_names = i['three_names']
        three_urls = i['three_urls']

        for three_name, three_url in zip(three_names, three_urls):
            try:
                spider.mongo_db.content_test_q.insert_one(
                    {
                        'second_name': i['second_name'],
                        'three_name': three_name,
                        'three_url': three_url
                    })

                spider.log('insert mongo succed!  three_name=%s, three_url=%s ' % (three_name, three_url), level=log.INFO)
            except pymongo.errors.DuplicateKeyError:
                spider.log('insert url is existed! ' , level=log.WARNING)
                continue
            except Exception, e:
                spider.log('insert mongo failed! (%s)' % (str(e)), level=log.ERROR)
