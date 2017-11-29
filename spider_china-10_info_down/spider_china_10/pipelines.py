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
        names = i['names']
        introduces = i['introduces']
        pics = i['pics']

        for name, introduce, pic in zip(names, introduces, pics):
            try:
                # spider.mongo_db.content_test_info.update_one(
                spider.mongo_db.content_test_n.insert_one(
                    {
                        'three_name': i['three_name'],
                        'three_url': i['three_url'],
                        'name': name,
                        'introduce': introduce,
                        'pic': pic
                    })

                spider.log('insert mongo succed!  name=%s ' % (name), level=log.INFO)
            except pymongo.errors.DuplicateKeyError:
                spider.log('insert url is existed! ' , level=log.WARNING)
                continue
            except Exception, e:
                spider.log('insert mongo failed! (%s)' % (str(e)), level=log.ERROR)
