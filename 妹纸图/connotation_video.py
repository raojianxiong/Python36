# coding=utf-8
import os
import time
import requests
import threading
from lxml import etree
from selenium import webdriver
from contextlib import closing
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VideoDown():

    def __init__(self):
        self.first_position = 0
        self.count = 0
        self.video_path = 'D:/Photo/VD/'
        self.threads = []
        self.content = []
        self.check_file()

    def check_file(self):
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

    def load_data(self):
        video_url = "http://neihanshequ.com/video/"
        driver = webdriver.Firefox()  # 获取浏览器驱动
        driver.maximize_window()
        driver.implicitly_wait(10)  # 隐式等待方法一定程度上节省了很多时间
        driver.get(video_url)

        while True:
            try:
                # WebDriverWait(driver, 10).until(
                #     lambda x: x.find_element_by_id('loadMore'))
                # or 通过定位器来定位元素
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'loadMore')))
            except Exception as e:
                print("WebDriverWait Error : ", str(e))
                break
            js='window.scrollTo(0,document.body.scrollHeight)'
            driver.execute_script(js)

            # 等待10秒，让浏览器加载
            time.sleep(10)

            source=etree.HTML(driver.page_source)
            divs=source.xpath('//*[@id="detail-list"]/li')
            for div in divs:
                self.count += 1
                print('第%d条数据' % self.count)
                title=div.xpath('./div/div[2]/a/div/p/text()')  # 这里xpath获取div/h1/p获取不到
                v_url=div.xpath('.//div[@class="player-container"]/@data-src')
                title=title[0] if len(title) > 0 else '无介绍'
                v_url=v_url[0] if len(v_url) > 0 else ""

                self.do_thread(title, v_url)

            try:
                load_more=WebDriverWait(driver, 10).until(
                    lambda x: x.find_element_by_id('loadMore'))
                load_more.click()
                time.sleep(10)
            except Exception as e:
                print("load more error : ", str(e))

    def do_thread(self, title, url):
        t=threading.Thread(target=self.down_video, args=(title, url))
        self.threads.append(t)
        t.start()

        for tt in self.threads:
            tt.join()

    def down_video(self, title, url):
        try:
            # 拿到原始返回数据
            with closing(requests.get(url, stream=True)) as response:
                print(url)
                chunk_size=1024
                content_size=int(response.headers['content-length'])

                file_name=self.video_path + '{}.mp4'.format(title)
                if os.path.exists(file_name) and os.path.getsize(file_name) == content_size:
                    print('跳过 ' + file_name)
                else:
                    down=DownProgress(title, content_size)
                    with open(file_name, 'wb') as f:
                        for data in response.iter_content(chunk_size=chunk_size):
                            f.write(data)
                            down.refresh_down(len(data))
        except Exception as e:
            print('error : ', str(e))


class DownProgress():

    def __init__(self, file_name, file_size):
        self.file_name=file_name
        self.file_down=0
        self.file_size=file_size

    def refresh_down(self, down):
        self.file_down=self.file_down + down
        progress=(self.file_down / float(self.file_size)) * 100
        status='下载完成 ' if self.file_down >= self.file_size else "正在下载"
        print('文件名称 : {}, 下载进度 : {}, 下载状态 : {}'.format(self.file_name,
                                                       '%.2f' % progress, status))


if __name__ == '__main__':
    start_time=time.time()
    down=VideoDown()
    down.load_data()
    end_time=time.time()
    print("下载共花费时间{}秒".format(end_time - start_time))
