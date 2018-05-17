# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from urllib import parse


def return_Exp(value):
    return "%s,%s" % (value[1], value[2])


def return_Loc(value):
    return value[0]


def return_Name(value):
    return value[0]


def return_JB(value):
    return value[0]


def return_Cate(value):
    return value[0]


def return_Fian(value):
    return value[1]


def return_NR(value):
    return value[1]


def deal_url(url):
    return parse.urljoin("https://www.zhipin.com/", url)


class BossItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BossjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()  # 公司名
    job = scrapy.Field()  # 工作职位
    salary = scrapy.Field()  # 薪水
    experience = scrapy.Field(
        # input_processor=MapCompose(return_Exp)
    )  # 经验 1- 3年

    situation = scrapy.Field(
        # input_processor=MapCompose(return_Cate)
    )  # 公司分类 融资 人数
    publish_time = scrapy.Field()  # 发布日期
    publish_person = scrapy.Field(
        # input_processor=MapCompose(return_Name)
    )  # 发布人 职位
    company_link = scrapy.Field(
        # input_processor=MapCompose(deal_url)

    )  # 公司链接

    # 此处先向数据库创建好表格,见DBHelper类
    def get_insert_sql(self):
        insert_sql = '''
        insert into boss(company_name,job,salary,experience,situation,
        publish_time,publish_person,
        company_link VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE salary=VALUES(salary),publish_time=VALUES(publish_time))
        '''
        params = (self['company_name'], self['job'], self['salary'], self['experience'],
                  self['situation'],  self['publish_time'],
                  self['publish_person'],
                  self['company_link'])
        return insert_sql, params
