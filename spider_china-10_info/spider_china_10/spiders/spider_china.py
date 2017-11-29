
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
    name = "spider_china_info"

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
            records = self.mongo_db.content_test_q.find({}, {'three_url': 1, 'three_name': 1})
            for record in records:
                three_url = record['three_url']
                three_name = record['three_name']

                meta = {'dont_redirect': True, 'three_url': three_url, 'three_name': three_name, 'dont_retry': True}
                yield scrapy.Request(url = three_url, meta = meta, callback = self.parse_final_page, dont_filter = True)
        except:
            self.log('start_request error! (%s)' % (str(traceback.format_exc())), level=log.INFO)


    ## 解析三级分类下信息
    def parse_final_page(self, response):
        sel = Selector(response)

        ret_item = SpiderChina10Item()
        ret_item['update_item'] = {}
        i = ret_item['update_item']

        i['three_name'] = response.meta['three_name']
        i['three_url'] = response.meta['three_url']
        # print i['three_name']

        names_xpaths = sel.xpath("//dl/dt/a[@class='fl bname font16']/text()").extract()
        if names_xpaths:
            i['names'] = names_xpaths
        else:
            i['names'] = ''

        introduce_xpaths = re.findall(u'(?<=<dd class="desc font12">).*?(?=\n)', response.body, re.S)
        introduce_xpaths = list(introduce_xpaths)
        # introduces = []
        # introduce_xpaths = sel.xpath("//dl/dd[@class='desc font12']/text()").extract()
        if introduce_xpaths:
            # for intro in introduce_xpaths:
                # introduce = re.findall('(?<=\().*?(?=\))', intro, re.S)
                # introduce = ''.join(introduce)
                # print introduce
                # # introduce = intro.strip().replace('\r\n', '').replace('[','').replace(']','').replace('\n','')
                # introduces.append(introduce)
            i['introduces'] = introduce_xpaths
        else:
            i['introduces'] = ''

        pics = []
        pics_xpaths = sel.xpath("//div[@class='img']/img/@src").extract()
        if pics_xpaths:
            for pic_xpath in pics_xpaths:
                global pic_gif
                pic_z = re.findall('(?<=http).*?(?=.gif)', pic_xpath)
                if pic_z:
                    pic_z = ''.join(pic_z)
                    pic_gif = 'http' + pic_z + '.gif'
                pics.append(pic_gif)
            i['pics'] = pics
        else:
            i['pics'] = ''

        self.log('#####  three_classify:, three_name:%s, names:%d, introduces:%d' % (i['three_name'], len(i['names']), len(i['introduces'])), level=log.INFO)
        yield ret_item

        # down_xpaths = sel.xpath("//div[@class='tjlogo']/a")
        # for down_xpath in down_xpaths:
            # down_url = down_xpath.xpath("@href")[0].extract()

            # meta = {'dont_redirect': True, 'item': i, 'dont_retry': True}
            # yield scrapy.Request(url = down_url, meta = meta, callback = self.parse_except_page, dont_filter = True)

