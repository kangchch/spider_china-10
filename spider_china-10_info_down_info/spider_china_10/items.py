# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderChina10Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    update_item = scrapy.Field()

    first_url = scrapy.Field()
    first_name = scrapy.Field()
    second_url = scrapy.Field()
    second_name = scrapy.Field()
    three_url = scrapy.Field()
    three_name = scrapy.Field()
    name = scrapy.Field()
    intrduce = scrapy.Field()
    picture = scrapy.Field()

    down_url = scrapy.Field()
