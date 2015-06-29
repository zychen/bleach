#!/usr/bin/env python
# coding=utf-8
"""
File: cataloguespider.py
Author: CHENZY
Date: 2015/06/15
"""
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from bleach.items import BleachItem
from bleach.pipelines import BleachPipeline
from scrapy.contrib.pipeline.images import ImagesPipeline


class catalogueSpider(scrapy.Spider):
    name = 'bleach'
    start_urls = ['http://www.7330.com/op/']
    base_urls = 'http://www.7330.com/op/'

    def parse(self, response):
        sel = Selector(response)
        episode_url = sel.xpath('//ul[@id="g1"]/li')

        episode_num = len(episode_url)
        for index, url in enumerate(episode_url):
            if index < 1:
                prefix = str(episode_num - index).zfill(4)
                episode_name = prefix + '_' + url.xpath('a/text()').extract()[0]
                item_url = url.xpath('a/@href').extract()[0]
                yield Request(url=item_url, callback=self.parse_item, meta={'episode_name': episode_name})

    def parse_item(self, response):
        episode_name = response.meta['episode_name']
        sel = Selector(response)
        pic_select_url = sel.xpath('//*[@id="p__select"][1]/option')

        for u in pic_select_url:
            # 必须在此处实例化BleachItem()
            # 如果在for循环之前或者是在 self.parse() 里面实例化，
            # 然后通过 meta 传过来，都不行，每一话中只能下载一张图片
            item = BleachItem()
            item['name'] = episode_name
            value = u.xpath('./@value').extract()[0]
            item_url = self.base_urls + value
            page_number = u.xpath('./text()').extract()[0]
            item['image_name'] = item['name'] + '_' + page_number.zfill(2)

            # 此处是处理第一张图片的问题
            # parse_item 获得的 response 就是第一页的内容
            # 第一页的图片地址通过分析本页即可获得-item['image_urls'] = sel.xpath('//*[@id="pictureContent"]//img/@src').extract()
            # 如果不处理，直接：yield Request(url=item_url, callback=self.parse_details, meta={'item': item})
            # 那么第一页 url=item_url 已经处理过了，scrapy 会忽略重复的url，从而造成第一张图缺失
            if page_number == '1':
                item['image_urls'] = sel.xpath('//*[@id="pictureContent"]//img/@src').extract()
                # 直接yield，返回item
                # 这样scrapy调度器就可以将item发送给Item Pipeline进行处理了
                yield item
                continue

            yield Request(url=item_url, callback=self.parse_details, meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        sel = Selector(response)
        item['image_urls'] = sel.xpath('//*[@id="pictureContent"]//img/@src').extract()
        return item






class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print "title: %s, link: %s, desc:%s" % (title, link, desc)
