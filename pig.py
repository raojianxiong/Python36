# coding=utf-8
from lxml import etree
import requests
import xlwt
import xlrd


class ZbjData(object):
    proxies = {
        'http': 'http://211.202.248.52:80'
    }

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    headers = {'User-Agent': user_agent}

    def __init__(self):
        self.f = xlwt.Workbook()#创建工作簿
        self.sheet1 = self.f.add_sheet("任务列表",cell_overwrite_ok=True)
        self.rowsTitle = ['编号','标题','简介','价格','截止日期','链接']
        for i in range(0,len(self.rowsTitle)):
            self.sheet1.write(0,i,self.rowsTitle[i],self.set_style('Times new Roman',220,True))
            
        self.f.save('zbj.xlsx')

    def set_style(self,name,height,bold=False):
        style = xlwt.XFStyle()#初始化样式
        font = xlwt.Font()#为样式创建字体
        font.bold = bold
        font.name = name
        font.colour_index = 2
        font.height = height
        style.font = font
        return style


    def get_url(self):
        print("=======开始")
        for i in range(5):
            url = "http://task.zbj.com/t-ppsj/p{}s5.html".format(i+1)
            self.spiderPage(url)
        print("整体结束Over")

    def spiderPage(self,url):
        if url is None:
            return None
        try:
            global headers, proxies
            htmlText = requests.get(url, headers=self.headers).text
            data = xlrd.open_workbook('zbj.xlsx')
            table = data.sheets()[0]
            rowCount = table.nrows

        
            selector = etree.HTML(htmlText)
            trs = selector.xpath("//*[@class='tab-switch tab-progress']/table/tr")
            m = 0
            for tr in trs:
                data = []#注意数据放在里面
                price = tr.xpath("./td[1]/p[1]/em/text()")
                href = tr.xpath("./td[1]/p[1]/a/@href")
                title = tr.xpath("./td[1]/p[1]/a/text()")
                subTitle = tr.xpath("./td[1]/p[2]/text()")
                lastData = tr.xpath("./td[4]/span/text()")
                if href[0].startswith('//'):
                    continue
                price = price[0] if len(price) >0 else ''
                href = href[0] if len(href) >0 else ''
                title = title[0] if len(title) >0 else ''
                subTitle = subTitle[0] if len(subTitle) >0 else ''
                lastData = lastData[0] if len(lastData) >0 else ''
                #拼接成一个集合
                data.append(rowCount+m)
                data.append(title)
                data.append(subTitle)
                data.append(price)
                data.append(lastData)
                data.append(href)

                for i in range(len(data)):
                    self.sheet1.write(rowCount+m,i,data[i])
                m+=1
                print("第%s行====="%m)
                print("项目:%s,简介：%s,价格：%s,截止日期:%s,详细地址:%s" %
                    (title, subTitle, price, lastData, href))
                print("\t---------------------------------------------")
                self.spiderDetail(href)

        except Exception as e:
            print("出错啦", str(e))
            self.f.save('zbj.xlsx')
            print("over!!")
        finally:
            self.f.save('zbj.xlsx')
            print("over!!")


    def spiderDetail(self,href):
        if href is None:
            return None
        try:
            htmlText = requests.get(href).text
            selector = etree.HTML(htmlText)
            detail = selector.xpath("//*[@id='utopia_widget_10']/div[2]/div/div[1]/div[1]/text()")[0]
            print("具体详情：\t", detail)
        except Exception as e:
            print("获取项目详情页出错了", str(e))

if '_main_':
    zbj = ZbjData()
    zbj.get_url()
    
# get_url()
