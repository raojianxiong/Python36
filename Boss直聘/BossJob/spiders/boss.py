# -*- coding: utf-8 -*-
import scrapy
from BossJob.items import BossjobItem, BossItemLoader
from urllib import parse


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['www.zhipin.com']

    # offset = 0  # page
    city = "c100010000/h_100010000"  # 查找的城市，后续可以指定，利用input输入
    job = "Python"  # 查找的岗位
    start_urls = ["https://www.zhipin.com/{0}/?query={1}&page=".format(city, job)]

    # start_urls = [baseURL]

    def parse(self, response):
        lis = response.css(".job-list ul li")
        for node in lis:
            item = BossjobItem()
            item['company_name'] = node.css('.company-text > h3 > a::text').extract_first("")
            item['job'] = node.css('div.job-title::text').extract_first("")
            item['salary'] = node.css('h3.name > a > span.red::text').extract_first("")
            item['experience'] = node.css('.info-primary > p::text').extract()  # 地址 经验 学历
            item['situation'] = node.css('.company-text > p::text').extract()  # 公司分类 融资 人数
            item['publish_time'] = node.css('.info-publis > p::text').extract_first("")  # 发布日期
            item['publish_person'] = node.css('.info-publis > h3::text').extract()  # 发布人 发布人的职位
            item['company_link'] = parse.urljoin('https://zhipin.com', node.css('.company-text > h3 a::attr(href)').extract_first(""))  # 记住需要拼接url

            yield item
            next_a = response.css('div.page > a.next::attr(href)').extract_first()
            print(next_a)
            if next_a != 'javascript:;':
                print("https://www.zhipin.com"+next_a)
                yield scrapy.Request("https://www.zhipin.com" + next_a, callback=self.parse)
