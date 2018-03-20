# coding=utf-8
"""
@author:SoS
@data:2018/3/19
@version:Python3.6
"""
import time
from lxml import etree
from urllib import parse
from Spider import Spider
from ExeclUtils import ExeclUtils


class JobXpath(Spider):
    def __init__(self):
        super(JobXpath, self).__init__()

    def parse_job_list(self, text):
        try:
            selector = etree.HTML(text)
            divs = selector.xpath('//div[@class="sojob-item-main clearfix"]')
            for div in divs:
                title = self.extract(div.xpath('./div[1]/h3/@title'))
                data = self.extract(div.xpath('./div[1]/p[1]/@title'))
                data = data.split("_")
                salary = data[0]
                region = data[1]
                degree = data[2]
                experience = data[3]
                name = self.extract(div.xpath('./div[2]/p[1]/a/text()'))
                industry = self.extract(
                    div.xpath('./div[2]/p[2]/span/a/text()'))
                href = self.extract(div.xpath('./div[1]/h3/a/@href'))

                self.append(title, salary, region, degree,
                            experience, name, industry)
                print(self.job_data)
                self.request_job_details(parse.urljoin(
                    'https://www.liepin.com', href))
                time.sleep(1)
        except Exception as e:
            print('parse_job_list error : {}'.format(e))

    def parse_job_details(self, text):
        try:
            selector = etree.HTML(text)
            data = selector.xpath('//div[@class="about-position"]/div[3]')
            # strip()不管用？
            detail = data[0].xpath('string(.)').replace(" ", "")
            if detail is "":
                self.job_data.append("职位无介绍")
            else:
                self.job_data.append(detail)
            self.count += 1
            ExeclUtils.write_execl(
                self.execl_f, self.sheet_info, self.count, self.job_data, "猎聘网_xpath.xlsx")
            print("crawel ", self.count, "条数据")
            self.data_clear()
        except Exception as e:
            print('parse_job_details error : {}'.format(e))
