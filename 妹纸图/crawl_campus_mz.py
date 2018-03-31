# coding=utf-8
'''
多进程爬虫，把继承类Process替换为Thread即为多线程爬虫
'''
import os
import time
from multiprocessing import Process, Pool
from requests_html import HTMLSession

class XHSpider(Process):
    def __init__(self,url):
        # 重写父类的__init__方法
        super(XHSpider, self).__init__()
        self.url = url

        self.session = HTMLSession()
        self.headers = {
            'Host':'news.daxues.cn',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.path = "D:/Photo/"
        self.check_file_path(self.path)

    def check_file_path(self, path):
        '''
        check the file is exists
        '''
        if not os.path.exists(path):
            os.makedirs(path)

    def run(self):
        self.parse_page()

    def send_request(self, url):
        '''
        用来发送请求的方法
        '''
        # 请求出错时，重复求情3次
        i = 0
        while i < 3:
            try:
                print('请求url : ', url)
                # 网页是utf-8编码
                return self.session.get(url, headers = self.headers).html
            except Exception as e:
                print('send_request error : ', str(e))
                i += 1

    def parse_page(self):
        '''
        解析网站源码,使用request-html提取
        '''
        html = self.send_request(self.url)
        imgs = html.find('dl a.p img')
        for img in imgs:
            href = img.attrs['src']
            alt = img.attrs['alt']
            self.save_image('http://news.daxues.cn'+href, alt)


    def save_image(self, url, name):
        '''
        save image
        '''
        content = self.session.get(url, headers=self.headers).content
        with open(self.path+name+'.jpg', 'wb') as f:
            f.write(content)
            f.close()
    def parse(self, url):
        self.url = url
        self.parse_page()

# 多进程、多线程爬取，只需要改继承类即可
def main():
    '''
    crawl data
    '''
    base_url = 'http://news.daxues.cn/xiaohua/ziliao/index{}.html'
    # 构造url_list
    url_list = [base_url.format(""), base_url.format("_2"), base_url.format("_3")]
    # 创建并启动进程
    process_list = []
    for url in url_list:
        p = XHSpider(url)
        p.start()
        process_list.append(p)

    for i in process_list:
        i.join()

# 线程池,想要使用此方法，先将XHSpider继承类去掉，包括super给注释掉
def pool_main():
    '''
    crawl data
    '''
    base_url = 'http://news.daxues.cn/xiaohua/ziliao/index{}.html'
    # 构造url_list
    url_list = [base_url.format(""), base_url.format("_2"), base_url.format("_3")]
    xh = XHSpider(url_list[0])
    p = Pool(4)
    for url in url_list:
        p.apply_async(xh.parse, args=(url,))
    
    p.close()
    p.join()


# 得出多进程花了2.2秒，多线程花了2.8秒，线程池花了2.4秒
if __name__ == '__main__':
    start = time.time()
    main()
    # pool_main()
    print('耗时 : %s'%(time.time() - start))
