# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class PublicspiderItem(ItemLoader):
    default_output_processor = TakeFirst()


def return_value(value):
    if value is None:
        return "无"
    return value


class PubliccommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 店铺名
    start = scrapy.Field()  # 几星商户
    taste = scrapy.Field()  # 口味
    environment = scrapy.Field()  # 环境
    service = scrapy.Field()  # 服务
    tag = scrapy.Field()  # 小吃快餐/创意菜/天津菜
    comments = scrapy.Field()  # 评论条数
    price = scrapy.Field()  # 人均消费
    area = scrapy.Field()  # 区域
    address = scrapy.Field()  # 地址
    recommend_food = scrapy.Field()  # 推荐菜
    has_bulk = scrapy.Field()  # 是否有团购
    preferential = scrapy.Field()  # 是否有优惠券
    link = scrapy.Field()  # 店铺地址链接
