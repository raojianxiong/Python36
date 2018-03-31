#coding=utf-8
"""
@author:JianxiongRao
@data:2018/3/10
@version:Python3.6
"""
import xlwt
import requests
from selenium import webdriver
import time
from lxml import etree
#通过模拟搜索页面并用xpath筛选岗位情况保存到excel中
class Job(object):
    def __init__(self):
        self.__url = 'http://www.51job.com' 
        self.__job = "Python"
        #记录excel中的行数,后面从第二行开始录入数据
        self.__count = 1
        #火狐驱动
        self.__driver = webdriver.Firefox()
        self.__createSheet()

    def __createSheet(self):
        #创建工作簿
        self.__f = xlwt.Workbook()
        self.__sheet = self.__f.add_sheet("51Job",cell_overwrite_ok=True)
        rowTitle = ['编号','标题','地点','公司名','待遇范围','工作简介','招聘网址']
        for i in range(0,len(rowTitle)):
            self.__sheet.write(0,i,rowTitle[i])
    
    #模拟查找对应工作搜索，这样就不用分析网页地址了
    def __findWebSite(self):
        self.__driver.get(self.__url)
        #最大化窗口
        self.__driver.maximize_window()

        self.__driver.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys(self.__job)
        #切换到全国查找，通过js设置没成功，只能换一种
        self.__driver.find_element_by_xpath('//*[@id="work_position_input"]').click()
        time.sleep(1)
        try:
            #定位当前地方
            self.__driver.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_050000"]/em').click()
        except:
            try:
                #可能帮你定到国外，这两种是常见的
                self.__driver.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_360000"]/em').click()
            except:
                print("您已设置为全国搜索了")
        self.__driver.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()
        #开始搜索进入到搜索页面
        self.__driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/button').click()
        time.sleep(1)
    
    #保存数据到excel中
    def __saveDataToExcel(self,jobs):
        for j in range(0,len(jobs)):
            self.__sheet.write(self.__count,j,jobs[j])
        self.__f.save("51Job_xpath.xlsx")
        self.__count += 1

    #对数据进行判断，并返回数组
    def __fitterField(self,title,address,name,salary,detail,site):
        jobs = []
        jobs.append(self.__count)
        title = title[0] if len(title) > 0 else ''
        jobs.append(title.strip())
        address = address[0] if len(address) > 0 else ''
        jobs.append(address)
        name = name[0] if len(name) > 0 else ''
        jobs.append(name)
        salary = salary[0] if len(salary) > 0 else ''
        jobs.append(salary)
        detail = detail if len(detail) > 0 else ''
        jobs.append(detail.strip())
        site = site[0] if len(site) > 0 else ''
        jobs.append(site)
        return jobs

    #工作简介职责
    def __getJobDetail(self,site):
        try:
            site = site[0] if len(site) > 0 else ''
            res = requests.get(site,timeout=2)
            res.encoding = 'gbk'
            selector = etree.HTML(res.text)
            #有时候是p标签组成的，有时候没有p标签
            jobDetails = selector.xpath('//div[@class="bmsg job_msg inbox"]')
            detail = jobDetails[0].xpath('string(.)').strip()
            print("div : ",detail)
            return detail
        except Exception as e:
            return "暂无数据"
            
          

    #获取51job上的数据
    def getData(self,work='Python'):
        self.__job=work
        #先模拟搜索全国Python招聘
        self.__findWebSite()
        while True:
            #下拉滚动条
            for i in range(5):
                height = 1000 * i
                self.__driver.execute_script('window.scrollBy(0,'+str(height)+')')
            selector = etree.HTML(self.__driver.page_source)
            divs = selector.xpath('//*[@id="resultList"]/div[@class="el"]')
            for div in divs:
                title = div.xpath('./p/span/a/text()')
                address=div.xpath('./span[2]/text()')
                name=div.xpath('./span[1]/a/@title')
                salary = div.xpath('./span[3]/text()')
                site = div.xpath('./p/span/a/@href')

                detail = self.__getJobDetail(site)
                
                jobs = self.__fitterField(title,address,name,salary,detail,site)
                #开始存入到excel中
                self.__saveDataToExcel(jobs)
            if selector.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a') == None:
                break
            self.__driver.find_element_by_xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a').click()

if __name__=='__main__':
    job = Job()
    #此处可以写Android等其它岗位
    job.getData('Python')

