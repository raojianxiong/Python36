#coding=utf-8
from selenium import webdriver
import time
from lxml import etree

'''
Pep8 python编程规范
https://www.douban.com/note/134971609/
'''
driver = webdriver.Firefox()
driver.maximize_window()
#20-30岁 女 本科
webUrl = 'http://www.lovewzly.com/jiaoyou.html'
driver.get(webUrl)

#毕竟网页需要加载
time.sleep(15)

#下拉滚动条
while True:
    for i in range(1,20):
        height = 1000 * i          
        strword = "window.scrollBy(0,"+str(height)+")"
        driver.execute_script(strword)
        time.sleep(3)
    htmlText = etree.HTML(driver.page_source)
    print(type(htmlText))
    selector = htmlText.xpath('//*[@class="result-box"]/table/tr/td/div')

    with open("妹纸统计.txt","a",encoding='UTF-8') as f:
        for div in selector:
            nick_name = div.xpath('./div[2]/p[1]/span/text()')
            age = div.xpath('./div[2]/p[2]/span[1]/text()')
            height = div.xpath('./div[2]/p[2]/span[2]/text()')
            location = div.xpath('./div[2]/p[2]/span[3]/text()')
            detail = div.xpath('./div[2]/p[3]/text()')
            photo = div.xpath('./div[1]/img/@src')
            
            nick_name = nick_name[0] if len(nick_name) > 0 else ''
            age = age[0] if len(age) > 0 else ''
            height = height[0] if len(height) > 0 else ''
            location = location[0] if len(location) > 0 else ''
            detail = detail[0] if len(detail) > 0 else ''
            photo = photo[0] if len(photo) > 0 else ''
            content = "昵称："+nick_name+" 年龄："+age+" 身高："+height+" 地址："+location+" 简介："+detail+" 照片："+photo
            print(content)
            f.write(content+"\n")
