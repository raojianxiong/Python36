#coding=utf-8
from selenium import webdriver
from lxml import etree
import time

username = "****"
pwd = "****"

driver = webdriver.Firefox()
driver.maximize_window()
# driver.get('https://weibo.com/login.php')

#开始登录操作
driver.find_element_by_id('loginname').send_keys(username)
driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(pwd)
#不记住用户
driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[5]/label/span').click()

driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
driver.get("https://weibo.com/p/1005051577826897/home?from=page_100505&mod=TAB&is_hot=1#place")

while True:
    #下拉滚动条
    for i in range(1,6):
        height = 2000*i
        strword = "window.scrollBy(0,"+str(height)+")"
        driver.execute_script(strword)
        time.sleep(5)
    
    selector = etree.HTML(driver.page_source)
    divs = selector.xpath('//*[@id="Pl_Official_MyProfileFeed__21"]/div/div')
    
    with open('feng_teacher.txt','a',encoding='utf-8') as f:
        for div in divs:
            content = div.xpath('./div[1]/div[4]/div[3]/text()')
            content = content[0] if len(content)>0 else ""
            content = content.strip()
            f.write(content+'\n')
            print(content)
            
    if driver.page_source.find('page next S_txt1 S_line1') == -1:
        print("已经是最后一页了")
        break;
    #需要登录自己的微博号
    driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__21"]/div/div[47]/div/a').click()
