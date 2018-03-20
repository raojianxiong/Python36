# coding=utf-8
"""
@author:SoS
@data:2018/3/20
@version:Python3.6
"""
import time
from urllib import parse
from Spider import Spider
from bs4 import BeautifulSoup
from ExeclUtils import ExeclUtils


class JobBs(Spider):
    def __init__(self):
        super(JobBs, self).__init__()

    def parse_job_list(self, text):
        try:
            soup = BeautifulSoup(text,'lxml')
            divs = soup.select('.sojob-item-main.clearfix')
            for div in divs:
                title = self.extract(div.select('.job-info > h3'))['title']
                href = self.extract(div.select('.job-info > h3 a'))['href']
                
                result = self.extract(div.select('.job-info > p'))
                if hasattr(result,'title'):
                    result = result['title'].split('_')
                else:
                    # 虽然不会出现
                    result = ['','','']
                salary = result[0]
                region = result[1]
                degree = result[2]
                experience = result[3]
                name = self.extract(div.select('.company-info.nohover > p a')).string
                industry = self.extract(div.select('.company-info.nohover .field-financing span a')).string
                self.append(title, salary, region, degree,experience, name, industry)
                print(self.job_data)
                self.request_job_details(parse.urljoin('https://www.liepin.com', href))
                time.sleep(1)
        except Exception as e:
            print("parse_job_list error :",str(e))

    def parse_job_details(self, text):
        try:
            soup2 = BeautifulSoup(text,'lxml')
            detail = soup2.select('.content.content-word')
            if detail:
                self.job_data.append(detail[0].get_text())
            else:
                self.job_data.append("暂无信息")
            self.count += 1
            ExeclUtils.write_execl(self.execl_f, self.sheet_info, self.count, self.job_data, "猎聘网_bs.xlsx")
            print("crawel ", self.count, "条数据")
            self.data_clear()
        except Exception as e:
            print("parse_job_details error : ",str(e))