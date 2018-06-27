# -*- coding: utf-8 -*-
import scrapy
from lagou.items import LagouItem
import logging


class LagouspiderSpider(scrapy.Spider):
    name = 'lagouspider'
    allowed_domains = ['www.lagou.com']
    url = 'https://www.lagou.com/zhaopin/Python/{page}/?filterOption=3'

    def start_requests(self):
        yield scrapy.Request(url=self.url.format(page=1), callback=self.parse, meta={'page': 1})

    def parse(self, response):
        logging.info('process:' + response.url)
        item_list = response.css('#s_position_list > .item_con_list > .con_list_item.default_list')
        if item_list:
            for resultitem in item_list:
                item = LagouItem()
                item['position'] = resultitem.css(
                    'div.list_item_top > div.position > div.p_top > a > h3::text').extract_first()
                item['location'] = resultitem.css(
                    'div.list_item_top > div.position > div.p_top > a > span > em::text').extract_first()
                item['money'] = resultitem.css(
                    'div.list_item_top > div.position > div.p_bot > div > span::text').extract_first()
                item['request'] = ''.join(
                    resultitem.css('div.list_item_top > div.position > div.p_bot > div::text').extract()).strip()
                item['company'] = resultitem.css(
                    'div.list_item_top > div.company > div.company_name > a::text').extract_first()
                item['tags'] = ','.join(resultitem.css('div.list_item_bot > div.li_b_l > span::text').extract())
                item['industry'] = resultitem.css(
                    'div.list_item_top > div.company > div.industry::text').extract_first().strip()
                item['advantage'] = resultitem.css('div.list_item_bot > div.li_b_r::text').extract_first()
                yield item
            if response.css(
                '#s_position_list > div.item_con_pager > div > a:last-child::attr(rel)').extract_first() != 'nofollow':
                page = response.meta.get('page') + 1
                yield scrapy.Request(url=self.url.format(page=page), callback=self.parse, meta={'page': page})
