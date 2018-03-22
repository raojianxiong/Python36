#coding=utf-8
import time
from selenium import webdriver
from lxml import etree

# 设置编码格式 默认以utf-8编码，写文件时，解码默认是anscii(py2)

friend = "****"
user = "****"
pw = "***"

# 获取浏览器驱动
driver = webdriver.Firefox()

# 浏览器窗口最大化
driver.maximize_window()

# 浏览器地址定向为qq登陆页面
driver.get("http://i.qq.com")

# 需要选中一下frame,否则找不到下面的网页元素,切换到login_frame框架
driver.switch_to.frame("login_frame")

# 自动点击账号登录方式
driver.find_element_by_id("switcher_plogin").click()

# 自动填充账户信息
driver.find_element_by_id('u').send_keys(user)
driver.find_element_by_id('p').send_keys(pw)

# 自动登录
driver.find_element_by_id('login_button').click()

# 让webdriver操纵当前页
driver.switch_to.default_content()

# 跳到说说的url,friend的空间可以自己顺便指定好友
driver.get('http://user.qzone.qq.com/'+friend+'/311')

next_num = 0  # 初始化下一页的id
while True:
    # 下拉滚动条,使得浏览器加载出动态加载的内容
    # 1 到 6 结束,分 5 次加载完每页的数据
    for i in range(1, 6):
        height = 2000 * i
        strWord = "window.scrollBy(0,"+str(height)+")"
        driver.execute_script(strWord)
        time.sleep(4)
    # 很多时候网页由多个<frame>或<iframe>组成，webdriver默认定位的是最外层的frame，
    # 所以这里需要选中一下说说所在的frame，否则找不到下面需要的网页元素
    driver.switch_to.frame("app_canvas_frame")
    selector = etree.HTML(driver.page_source)
    divs = selector.xpath('//*[@id="msgList"]/li/div[3]')

    #追加数据到文件末尾
    with open('qq_word.txt','a',encoding='utf-8') as f:
        for div in divs:
            qq_name = div.xpath('./div[2]/a/text()')
            qq_content = div.xpath('./div[2]/pre/text()')
            qq_time = div.xpath('./div[4]/div[1]/span/a/text()')
            qq_name = qq_name[0] if len(qq_name) >0 else ''
            qq_content = qq_content[0] if len(qq_content) else ''
            qq_time = qq_time[0] if len(qq_time) > 0 else ''
            print(qq_name,qq_content,qq_time)
            f.write(qq_content+"\n")
    
    #当已经到了尾页，下一页按钮id就没有了，可以停止了
    if driver.page_source.find('pager_next_'+str(next_num)) == -1:
        break
    #找下一页按钮
    driver.find_element_by_id('pager_next_'+str(next_num)).click()

    next_num += 1
    #跳到外层frame上,因为首先需要把页面拉下来
    driver.switch_to.parent_frame()