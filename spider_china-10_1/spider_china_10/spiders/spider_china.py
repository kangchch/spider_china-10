
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
    name = "spider_china_1"

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
            start_url = 'http://www.china-10.com'
            yield scrapy.Request(url = start_url, callback = self.parse_first_page, dont_filter = True)
        except:
            self.log('start_request error! (%s)' % (str(traceback.format_exc())), level=log.INFO)

    # 解析一级页面
    def parse_first_page(self, response):
        sel = Selector(response)

        ret_item = SpiderChina10Item()
        ret_item['update_item'] = {}
        i = ret_item['update_item']


        if response.status != 200 or len(response.body) <= 0:
            self.log('fetch failed ! status = %d, ' % (response.status), level = log.WARNING)

        first_xpaths = sel.xpath("//*[@id='conmenu']/li") ## 一级分类
        for first_xpath in first_xpaths:

            i['first_name'] = first_xpath.xpath("a/text()").extract()[1] ## 一级分类name
            i['first_url'] = first_xpath.xpath("a/@href").extract()[0] ## 一级分类url


            self.log('!!!!!  first_classify:, first_url:%s ' % (i['first_url']), level=log.INFO)
            meta = {'dont_redirect': True, 'item': ret_item, 'dont_retry': True}
            yield scrapy.Request(url = i['first_url'], meta = meta, callback = self.parse_second_page, dont_filter = True)


    # 解析二级页面
    def parse_second_page(self, response):
        sel = Selector(response)

        ret_item = response.meta['item']
        i = ret_item['update_item']

        second_xpaths = sel.xpath("//ul/li/a[@class='red dhidden']") ## 二级分类
        for second_xpath in second_xpaths:
            i['second_names'] = second_xpath.xpath("text()").extract() ## 二级类目名称
            i['second_urls'] = second_xpath.xpath("@href").extract() ## 二级类目url

            self.log('@@@@@  second_classify:, second_names:%d, second_Urls:%d ' % (len(i['second_names']), len(i['second_urls'])), level=log.INFO)
            # meta = {'dont_redirect': True, 'item': ret_item, 'dont_retry': True}
            yield ret_item

