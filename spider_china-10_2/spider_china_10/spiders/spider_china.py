
# -*- coding: utf-8 -*-
##
# @file spider_china.py
# @brief www.china-10.com
# @author kangchch
# @version 1.0
# @date 2017-11-21


from scrapy.http import Request
import xml.etree.ElementTree
from scrapy.selector import Selector

import scrapy
import re
from pymongo import MongoClient
from copy import copy
import traceback
import pymongo
from scrapy import log
from spider_china_10.items import SpiderChina10Item
import time
import datetime
import sys
import logging
import random
import binascii
from scrapy.conf import settings
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderChina10Spider(scrapy.Spider):
    name = "spider_china_2"

    def __init__(self, settings, *args, **kwargs):
        super(SpiderChina10Spider, self).__init__(*args, **kwargs)
        self.settings = settings
        mongo_info = settings.get('MONGO_INFO', {})

        try:
            self.mongo_db = pymongo.MongoClient(mongo_info['host'], mongo_info['port']).china_info
        except Exception, e:
            self.log('connect mongo 192.168.60.65:10010 failed! (%s)' % (str(e)), level=log.CRITICAL)
            raise scrapy.exceptions.CloseSpider('initialization mongo error (%s)' % (str(e)))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def start_requests(self):

        try:
            records = self.mongo_db.content_test_j.find({}, {'second_url': 1, 'second_name': 1})
            for record in records:
                second_url = record['second_url']
                second_name = record['second_name']

                meta = {'dont_redirect': True, 'second_name': second_name, 'second_url': second_url, 'dont_retry': True}
                yield scrapy.Request(url = second_url, meta = meta, callback = self.parse_three_page, dont_filter = True)
        except:
            self.log('start_request error! (%s)' % (str(traceback.format_exc())), level=log.INFO)


    # 解析三级页面
    def parse_three_page(self, response):
        sel = Selector(response)

        ret_item = SpiderChina10Item()
        ret_item['update_item'] = {}
        i = ret_item['update_item']

        i['second_name'] = response.meta['second_name']

        three_xpaths = sel.xpath("//ul/li/a[@class='red dhidden']") ## 三级分类
        for three_xpath in three_xpaths:
            i['three_names'] = three_xpath.xpath("text()").extract()  ## 三级类目名称
            i['three_urls'] = three_xpath.xpath("@href").extract()  ## 三级类目url

            self.log('#####  three_classify:, second_name:%s, three_names:%d, three_urls:%d' % (i['second_name'], len(i['three_names']), len(i['three_urls'])), level=log.INFO)
            meta = {'dont_redirect': True, 'item': ret_item, 'dont_retry': True}
            yield ret_item
            # yield scrapy.Request(url = i['three_url'], meta = meta, callback = self.parse_final_page, dont_filter = True)

