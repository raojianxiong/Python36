#coding=utf-8
"""
@author:JianxiongRao
@data:2018/3/12
@version:Python3.6
"""
from requests_html import HTMLSession
import os
import time

class MM(object):
    def __init__(self):
        self.__page = 1
        self.__url = "http://www.mm131.com/qingchun/list_1_{}.html"
        self.__session = HTMLSession()
        self.__headers = {
            'Referer':'http://www.mm131.com/qingchun/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
        self.__imagePath = r'D:/Photo/MM'
        self.__confirmPath()

    def __confirmPath(self):
        if not os.path.exists(self.__imagePath):
            os.makedirs(self.__imagePath)
            
    def download(self,link,fileName):
        try:
            with open(self.__imagePath+'/'+fileName+'.jpg','wb') as f:
                f.write(self.__session.request('get',link,headers = self.__headers,allow_redirects=False).content)
        except Exception as e:
            print(str(e))

    def parseData(self):
        start = time.time()
        while self.__page < 12:
            if self.__page == 1:
                self.__url = "http://www.mm131.com/qingchun/"
            else:
                self.__url = 'http://www.mm131.com/qingchun/list_1_{}.html'.format(self.__page)
            r = self.__session.get(self.__url)
            main = r.html.find(".main",first=True)
            dl = main.find('dl')[0]
            dds = dl.find('dd')
            for dd in dds[:-1]:
                attr = dd.find('img')[0].attrs
                imageLink = attr['src']
                title = attr['alt']
                self.download(imageLink,title)
            self.__page += 1
        end = time.time() - start
        print("爬取时间:",end)

if __name__=="__main__":
    mm = MM()
    mm.parseData()


