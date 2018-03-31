#coding=utf-8
"""
@author:JianxiongRao
@data:2018/3/10
@version:Python3.6
"""
import xlwt
import requests
import re


class Job(object):
    def __init__(self):
        self.__job = 'Python'
        self.__url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        self.__count = 1
        #总共672页
        self.__page = 1
        #总共672页
        self.__createSheet()

    def __createSheet(self):
        # 创建工作簿
        self.__f = xlwt.Workbook()
        self.__sheet = self.__f.add_sheet("51Job", cell_overwrite_ok=True)
        rowTitle = ['编号', '标题', '地点', '公司名', '待遇范围', '工作简介', '招聘网址']
        for i in range(0, len(rowTitle)):
            self.__sheet.write(0, i, rowTitle[i])

    # 保存数据到excel中
    def __saveDataToExcel(self, title, address, name, salary, detail, site):
        jobs = []
        jobs.append(self.__count)
        jobs.append(title)
        jobs.append(address)
        jobs.append(name)
        jobs.append(salary)
        jobs.append(detail)
        jobs.append(site)

        for j in range(0, len(jobs)):
            self.__sheet.write(self.__count, j, jobs[j])
        self.__f.save("51Job_re.xlsx")
        self.__count += 1

    # 访问详情页面
    def __getDetails(self, site):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        try:
            res = requests.get(site, headers=headers,timeout=1)
            res.encoding = 'gbk'
            pattern2 = re.compile('<div class.*?bmsg.*?job.*?msg.*?inbox">(.*?)</div>', re.S)
            details = re.findall(pattern2, res.text)
            print(details)
            if details is not None and len(details) != 0:
                details = re.sub(re.compile(r'<[^>]+>', re.S), '', details[0])
            else:
                details = "暂无数据"
        except:
            details = "暂无数据"
        return details

    def getData(self, work='Python'):
        try:
            self.__job = work
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
            while self.__page <= 672:
                url = self.__url.format(self.__job, self.__page)
                response = requests.get(url, headers=headers,timeout=1)
                response.encoding = 'gbk'
                content = response.text
                print(content)
                print("Start")
                pattern = re.compile('<div class="el">.*?<a.*?title="(.*?)".*?href="(.*?)".*?<a.*?title="(.*?)".*?class.*?"t3">(.*?)</span>.*?class.*?"t4">(.*?)</span>.*?</div>',re.S)
                print("go on")
                datas = re.findall(pattern,content)
                print("end")
                for each in datas:
                    title = ""
                    address = ""
                    name = ""
                    salary = ""
                    site = ""
                    details = ""
                    if len(each) == 0:
                        print("无数据")
                    else:
                        title = each[0]
                        address = each[3]
                        name = each[2]
                        salary = each[4]
                        site = each[1]
                        details = self.__getDetails(site)

                    self.__saveDataToExcel(title, address, name, salary, details, site)
                self.__page += 1
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    job = Job()
    job.getData()
