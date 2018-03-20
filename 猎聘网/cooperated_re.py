# coding=utf-8
"""
@author:SoS
@data:2018/3/20
@version:Python3.6
"""
import re
import time
from urllib import parse
from Spider import Spider
from ExeclUtils import ExeclUtils


class JobRe(Spider):
    def __init__(self):
        super(JobRe, self).__init__()

    def parse_job_list(self, text):
        try:
            pattern = re.compile('<div class="job-info">'
                                 '.*?<h3.*?title="(.*?)">.*?<a href="(.*?)".*?title="(.*?)">.*?<p class="company-name">.*?>(.*?)</a>.*?<p class="field-financing">.*?target="_blank">(.*?)</a>.*?</span>', re.S)
            datas = re.findall(pattern, text)
            for data in datas:
                title = data[0]
                href = data[1]
                result = data[2].split('_')
                salary = result[0]
                region = result[1]
                degree = result[2]
                experience = result[3]
                name = data[3]
                industry = data[4]
                self.append(title, salary, region, degree,
                            experience, name, industry)
                print(self.job_data)
                self.request_job_details(parse.urljoin(
                    'https://www.liepin.com', href))
                time.sleep(1)
        except Exception as e:
            print("re parse_job_list error : ", str(e))

    def parse_job_details(self, text):
        try:
            pattern = re.compile(
                '<div class="content content-word">(.*?)</div>.*?<div class="job-item main.*?">', re.S)
            text = re.search(pattern, text)
            detail = re.sub(re.compile('<[^>]+>', re.S), '', text.group(1))
            if detail:
                self.job_data.append(detail)
            else:
                self.job_data.append("暂无职位信息")
            self.count += 1
            ExeclUtils.write_execl(self.execl_f, self.sheet_info, self.count, self.job_data, "猎聘网_re.xlsx")
            print("crawel ", self.count, "条数据")
            self.data_clear()
        except Exception as e:
            print("re parse_job_list error : ", str(e))
