# coding=utf-8
"""
@author:JianxiongRao
@data:2018/3/10
@version:Python3.6
"""
import xlwt
import requests
from bs4 import BeautifulSoup

class Job(object):
    def __init__(self):
        self.__job = 'Python'
        self.__url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        self.__count = 1
        self.__page = 1
        self.__createSheet()

    def __createSheet(self):
        # 创建工作簿
        self.__f = xlwt.Workbook()
        self.__sheet = self.__f.add_sheet("51Job", cell_overwrite_ok=True)
        rowTitle = ['编号', '标题', '地点', '公司名', '待遇范围', '工作简介', '招聘网址']
        for i in range(0, len(rowTitle)):
            self.__sheet.write(0, i, rowTitle[i])

    # 保存数据到excel中
    def __saveDataToExcel(self,title,address,name,salary,detail,site):
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
        self.__f.save("51Job_bs4.xlsx")
        self.__count += 1

    def getData(self, work='Python'):
        self.__job = work
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        while self.__page <=672:    
            url = self.__url.format(self.__job, self.__page)   
            response = requests.get(url,headers = headers)
            response.encoding='gbk'
            html = response.text
            soup = BeautifulSoup(html,'lxml')
            #还有、、除此之外还可以直接用soup.select('.t1 span a')等,循环取出数据即可
            divs = soup.select("#resultList > div")
            #去掉开头的那三个div还有后面那三个
            for div in divs[3:-4]:
                title = div.p.span.a['title']
                spans = div.find_all("span")
                name = spans[1].a['title']
                address = spans[2].string
                salary = spans[3].string
                site = div.p.span.a['href']
                p_data = []
                #此处捕获异常是因为可能有些给的工作详情页不一样，当然也可以在异常中解析，不过有n多种可能
                try:
                    res = requests.get(site,headers=headers,timeout=2)
                    res.encoding = 'gbk'
                    soup2 = BeautifulSoup(res.text,'lxml')
                    div = soup2.find('div',attrs={"class":"bmsg job_msg inbox"})
                    print(div)
                    print('=============================')
                    if div is not None and len(div) != 0:
                        ps = div.find_all('p')
                        print(ps)
                        print(type(ps))
                        #存在p节点
                        for p in ps:
                            p_data.append(p.string)
                    else:
                        p_data.append(div.get_text().strip())
                except Exception as e:
                    print(str(e))
                    p_data.append("暂无")
                if len(p_data) !=0 and p_data[0] is None: p_data[0] = ""
                detail = ""
                try:
                    detail = "".join(p_data)
                except:
                    detail = "无数据"
                self.__saveDataToExcel(title,address,name,salary,detail,site)
            self.__page += 1

if __name__=='__main__':
    job = Job()
    #此处可以写Android等其它岗位
    job.getData('Python')