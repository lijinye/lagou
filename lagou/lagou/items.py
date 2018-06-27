# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LagouItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='lagou'
    position=Field()
    location=Field()
    money=Field()
    request = Field()
    company = Field()
    tags = Field()
    industry = Field()
    advantage = Field()
    # _id=Field()