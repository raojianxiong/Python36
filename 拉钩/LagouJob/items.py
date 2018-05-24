# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import scrapy
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from LagouJob.settings import SQL_DATETIME_FORMAT
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def replace_splash(value):
    return value.replace("/", "")


def handle_strip(value):
    return value.strip()


def handle_jobaddr(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


def handle_publish_time(value):
    return value.strip()


class LagoujobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    job_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field(
        input_processor=MapCompose(handle_publish_time)
    )
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_strip)
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    crawl_time = scrapy.Field()

    # 这样写，每个item都有其对应的语句，后续扩展方便
    def get_insert_sql(self):
        insert_sql = """
            insert into lagou(url, job_id, title, salary, job_city, work_years, degree_need, job_type,
            publish_time, tags, job_advantage, job_desc, job_addr, company_url, company_name, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), work_years=VALUES(work_years), 
            publish_time=VALUES(publish_time), job_desc=VALUES(job_desc)
        """
        params = (self["url"], self["job_id"], self["title"], self["salary"], self["job_city"], self["work_years"]
                  , self["degree_need"], self["job_type"], self["publish_time"], self["tags"], self["job_advantage"],
                  self["job_desc"], self["job_addr"], self["company_url"], self["company_name"],
                  self["crawl_time"].strftime(SQL_DATETIME_FORMAT))
        return insert_sql, params
