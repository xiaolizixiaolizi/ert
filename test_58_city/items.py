# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Test58CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class City58XiaoQu(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    reference_price=scrapy.Field()
    address=scrapy.Field()
    times=scrapy.Field()

class City58ItemZhuCu(scrapy.Item):
    id=scrapy.Field()
    name=scrapy.Field()
    zu_price=scrapy.Field()
    type=scrapy.Field()
    mianji=scrapy.Field()
    url=scrapy.Field()
    price_per=scrapy.Field()