# coding=utf-8
"""
@author:SoS
@data:2018/4/3
@version:Python3.6
"""
import requests
from datetime import datetime
import time
from PIL import Image
from selenium import webdriver

class jd():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def request_jd(self):
        user_name = input("请输入用户名\n")
        pwd = input("请输入密码\n")
        self.driver.maximize_window()
        self.driver.get("https://www.jd.com/")
        time.sleep(1)
        self.driver.find_element_by_class_name("link-login").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("账户登录").click()
        self.jd_cookies = self.driver.get_cookies()
        self.driver.find_element_by_id("loginname").send_keys(user_name)
        self.driver.find_element_by_id("nloginpwd").send_keys(pwd)
        
        try:
            self.driver.find_element_by_css_selector(".btn-img.btn-entry").click()
            time.sleep(0.5)
        
            print("需要输入验证码")
            # 可能有验证码
            captcha = self.request_capture()
            print("验证码",captcha)
            time.sleep(0.5)
            self.driver.find_element_by_id("authcode").send_keys(captcha)
            time.sleep(0.5)
            self.driver.find_element_by_css_selector(".btn-img.btn-entry").click()
        except:
            print("验证码")
        
        self.driver.get("https://item.jd.com/4255683.html")
        time.sleep(1)
        self.driver.find_element_by_id("InitCartUrl")
        try:
            self.driver.find_element_by_id("btn-onkeybuy").click()
        except :
            # 没有货了，继续刷30次
            count = 0
            while count < 30:
                self.driver.get("https://item.jd.com/4255683.html")
                try:
                    # 抢购
                    self.driver.find_element_by_id("choose-btn-ko").click()
                    break
                except:
                    count+=1
                    

        self.driver.find_element_by_id("order-submit").click()
        time.time(1)
        print("over")

    # 获取验证码并把图片显示出来
    def request_capture(self):
        headers = {
            "Referer":"https://www.jd.com/",
            "User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/53"
        }
        try:
            capture_url = self.driver.find_element_by_css_selector("#JD_Verification1").get_attribute("src2")
            # capture_url = capture_url + "&yys="+str(int(time.time()))
            print(capture_url)
            session = requests.Session();
            # cookies = requests.utils.cookiejar_from_dict(self.cookies_to_dict(),cookiejar=None, overwrite=True)
            # session.cookies = cookies
            response = session.get("https:"+capture_url, headers=headers, allow_redirects=False)
            with open("captcha.jpg","wb") as f:
                print(type(response.content))
                f.write(response.content)
                f.close()
        
            im = Image.open("captcha.jpg")
            im.show()
            im.close()
            captcha = input("请输入验证码\n")
            return captcha
        except:
            print("无验证码")
            return input("请输入验证码\n")
           
    # Selenium cookies 转换成字典类型设置给 requests
    def cookies_to_dict(self):
        cookie =[item["name"] + ":" + item["value"] for item in self.jd_cookies]
        cookies = ';'.join(item for item in cookie) 
        cook_map = {}
        for item in cookie :
          str = item.split(':')
          cook_map[str[0]] = str[1]
        return cook_map

if __name__ == "__main__":
    jd = jd()
    jd.request_jd()
