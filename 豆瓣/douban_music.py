#coding=utf-8
'''
data数据需要全局
'''
from lxml import etree
import requests
import pandas as pd

data = {'href':[],'title':[],'score':[],'number':[],'img':[]}
def _getUrl():
    for i in range(10):
        url = "https://music.douban.com/top250?start={}".format(i*25)
        scrapyPage(url)
def scrapyPage(url):
    html = requests.get(url).text
    s = etree.HTML(html)
    trs = s.xpath("//*[@id='content']/div/div[1]/div/table/tr")
    global data
    for tr in trs:
        href = tr.xpath("./td[2]/div/a/@href")[0]
        title = tr.xpath("./td[2]/div/a/text()")[0]
        score = tr.xpath("./td[2]/div/div/span[2]/text()")[0]
        number = tr.xpath("./td[2]/div/div/span[3]/text()")[0]
        img = tr.xpath("./td[1]/a/img/@src")[0]
        print(href,title,score,number,img)
        
        data['href'].append(href)
        data['title'].append(title)
        data['score'].append(score)
        data['number'].append(number)
        data['img'].append(img)
    __writeDataToExcel(data)
def __writeDataToExcel(data):
    pdf = pd.DataFrame(data)
    pdf.to_excel('excel_douban.xlsx',index=False,sheet_name='豆瓣音乐')
    print("save over !!")

if __name__ == '__main__':
    _getUrl()


