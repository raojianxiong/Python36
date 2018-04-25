# coding=utf-8
"""
@author:SoS
@data:2018/3/19
@version:Python3.6
"""
from cooperated_re import JobRe
from cooperated_bs import JobBs
from cooperated_xpath import JobXpath

class Main():
    @staticmethod
    def select_type():
        type = input('请输入爬虫类型:\n1.xpath\n2.BeatuifulSoup4\n3.re\n')
        try:
            type = int(type)
        except:
            print("请您正确输入")
        print("您已输入 ", type)
        if type == 1:
            print("开始xpath爬取数据....")
            xpath = JobXpath()
            xpath.crawler_data()
        elif type == 2:
            print("开始bs4爬取数据....")
            bs = JobBs()
            bs.crawler_data()
        else:
            print("开始re爬取数据")
            re = JobRe()
            re.crawler_data()
        print("爬取完毕")


if __name__ == '__main__':
    Main.select_type()
