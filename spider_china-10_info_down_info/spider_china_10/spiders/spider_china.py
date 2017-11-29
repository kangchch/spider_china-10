
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
    name = "spider_china_info_down_info"

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
            records = self.mongo_db.content_test_down_url.find({}, {'down_url': 1, 'three_name': 1})
            for record in records:
                down_url = record['down_url']
                three_name = record['three_name']

                meta = {'dont_redirect': True, 'down_url': down_url, 'three_name': three_name, 'dont_retry': True}
                yield scrapy.Request(url = down_url, meta = meta, callback = self.parse_down_page, dont_filter = True)
        except:
            self.log('start_request error! (%s)' % (str(traceback.format_exc())), level=log.INFO)


    def parse_down_page(self, response):
        sel = Selector(response)

        ret_item = SpiderChina10Item()
        ret_item['update_item'] = {}
        i = ret_item['update_item']

        i['down_url'] = response.meta['down_url']
        i['three_name'] = response.meta['three_name']

        names_xpaths = sel.xpath("//em[@class='font12 fff dhidden']/text()").extract()
        if names_xpaths:
            i['names'] = names_xpaths
        else:
            i['names'] = ''

        introduce_xpaths = sel.xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/div[1]/div[2]/div/text()').extract()
        introduces = []
        if introduce_xpaths:
            for inc in introduce_xpaths:
                introduce = inc.strip().replace('\r\n','').replace('\n','')
                introduces.append(introduce)

            i['introduces'] = introduces
        else:
            i['introduces'] = ''

        pics_xpaths = sel.xpath("//div[@class='img']/a/div[@class='imgbox']/img/@src").extract()
        if pics_xpaths:
            i['pics'] = pics_xpaths
        else:
            i['pics'] = ''

        self.log('#####  three_classify:, three_name:%s, names:%d, introduces:%d' % (i['three_name'], len(i['names']), len(i['introduces'])), level=log.INFO)
        yield ret_item
