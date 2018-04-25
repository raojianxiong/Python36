# coding=utf-8
"""
@author:SoS
@data:2018/3/19
@version:Python3.6
"""
import abc
import time
import requests
from ExeclUtils import ExeclUtils

# abstract class
class Spider():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.row_title = ['标题','待遇','地区','学历要求','经验','公司名称','所属行业','职位描述']
        sheet_name = "猎聘网"
        self.execl_f, self.sheet_info = ExeclUtils.create_execl(sheet_name,self.row_title)
        # add element in one data
        self.job_data = []
        # the data added start with 1
        self.count = 0

    def crawler_data(self):
        '''
        crawler data
        '''
        for i in range(0,5):
            url = 'https://www.liepin.com/zhaopin/?industryType=&jobKind=&sortFlag=15&degradeFlag=0&industries=&salary=&compscale=&key=Python&clean_condition=&headckid=4a4adb68b22970bd&d_pageSize=40&siTag=p_XzVCa5J0EfySMbVjghcw~fA9rXquZc5IkJpXC-Ycixw&d_headId=62ac45351cdd7a103ac7d50e1142b2a0&d_ckId=62ac45351cdd7a103ac7d50e1142b2a0&d_sfrom=search_fp&d_curPage=0&curPage={}'.format(i)
            self.request_job_list(url)
            time.sleep(2)   

    def request_job_list(self,url):
        '''
        get the job data by request url
        '''
        try:
            headers = {
                'Referer':'https://www.liepin.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
            }
            reponse = requests.get(url,headers = headers)
            # utf-8
            if reponse.status_code != 200:
                return
            self.parse_job_list(reponse.text)
        except Exception as e:
            # raise e
            print('request_job_list error : {}'.format(e))

    @abc.abstractmethod
    def parse_job_list(self,text):
        '''
        parsing the data from the response
        '''
        pass
    
    def request_job_details(self,url):
        '''
        request thr job detail's url
        '''
        try:
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
            }
            response = requests.get(url,headers = headers);
            # utf-8
            if response.status_code != 200:
                return
            self.parse_job_details(response.text)
        except Exception as e:
            # raise e
            print('request_job_details error : {}'.format(e))
        
    @abc.abstractmethod
    def parse_job_details(self,text):
        '''
        parsing the job details from text
        '''
        pass

    def append(self,title,salary,region,degree,experience,name,industry):
        self.job_data.append(title)
        self.job_data.append(salary)
        self.job_data.append(region)
        self.job_data.append(degree)
        self.job_data.append(experience)
        self.job_data.append(name)
        self.job_data.append(industry)
    
    def data_clear(self):
        self.job_data = []

    def extract(self, data):
        return data[0] if len(data) > 0 else ""
