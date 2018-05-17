# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class BossjobPipeline(object):

    def __init__(self):
        self.count = 1
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet("Boss直聘", cell_overwrite_ok=True)
        # 13列
        row_title = ['公司名', '职位', "薪水", "工作地点/要求", "所属行业/融资/人数", "发布日期", "发布人/职位", "公司链接"]
        for i in range(0, len(row_title)):
            self.sheet.write(0, i, row_title[i])

    def process_item(self, item, spider):
        craw_list = list()
        craw_list.append(item["company_name"])
        craw_list.append(item["job"])
        craw_list.append(item["salary"])
        craw_list.append(item["experience"])

        craw_list.append(item["situation"])
        craw_list.append(item["publish_time"])
        craw_list.append(item["publish_person"])

        craw_list.append(item["company_link"])

        self.write_in_excel(craw_list)
        return item

    def write_in_excel(self, crawl_list):
        for j in range(0,len(crawl_list)):
            self.sheet.write(self.count, j, crawl_list[j])
        self.workbook.save("Boss直聘.xlsx")
        self.count += 1


class BossJobMySql(object):
    def __init__(self, dbpool):
        self.dppool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",  # 此处可能填写utf-8 数据库会连接失败，报错
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  # 这里使用变长参数

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dppool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def handle_error(self, failure, item, spider):
        print(failure)
