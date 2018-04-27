# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class PubliccommentPipeline(object):

    def __init__(self):
        self.count = 1
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet("大众点评", cell_overwrite_ok=True)
        # 14列
        row_title = ["店铺名", "星级", "口味", "环境", "服务", "菜的类型", "评论数量", "人均消费", "区域", "地址", "推荐菜", "是否有团购", "是否有优惠券", "店铺链接"]
        for i in range(0, len(row_title)):
            self.sheet.write(0, i, row_title[i])

    def process_item(self, item, spider):
        crawl_list = list()

        crawl_list.append(item['name'])
        crawl_list.append(item['start'])
        crawl_list.append(item['taste'])
        crawl_list.append(item['environment'])
        crawl_list.append(item['service'])
        crawl_list.append(item['tag'])
        crawl_list.append(item['comments'])
        crawl_list.append(item['price'])
        crawl_list.append(item['area'])
        crawl_list.append(item['address'])
        crawl_list.append(item['recommend_food'])
        crawl_list.append(item['has_bulk'])
        crawl_list.append(item['preferential'])
        crawl_list.append(item['link'])

        self.write_in_excel(crawl_list)
        return item

    def write_in_excel(self, crawl_list):
        for j in range(0, len(crawl_list)):
            self.sheet.write(self.count, j, crawl_list[j])
        self.workbook.save("大众点评.xlsx")
        self.count += 1
