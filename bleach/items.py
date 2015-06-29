# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BleachItem(Item):
    name = Field()
    image_urls = Field()
    image_name = Field()
