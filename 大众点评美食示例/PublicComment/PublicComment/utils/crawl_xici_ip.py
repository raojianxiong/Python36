# -*- coding:utf-8 _*-  
""" 
@author:Jianxiong Rao 
@file: crawl_xici_ip.py 
@time: 2018/04/05 
"""
import requests
from scrapy.selector import Selector



def crawl_ips():
    # 爬取西刺免费的ip代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    # 这是第一页
    for i in range(2852):
        re = requests.get("http://www.xicidaili.com/nn/{}".format(i), headers=headers)

        ip_list = []
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_tds = tr.css("td")
            ip = all_tds[1].css("::text").extract()[0]
            port = all_tds[2].css("::text").extract()[0]
            proxy_type = all_tds[5].css("::text").extract()[0]
            ip_list.append((ip, port, proxy_type, speed))
    return ip_list


class GetIp(object):

    def delete_ip(self, ip, iplist):
        iplist.remove(ip)

    def judge_ip(self, ip, port, proxy_type,iplist):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "https://{1}:{2}".format(ip, port)
        proxy_dict = {
            proxy_type: proxy_url
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip,iplist)
            return False
        else:
            code = response.status_code
            if 200 <= code <= 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip,iplist)
                return False

    def get_random_ip(self):
        iplist = crawl_ips()
        for ip_info in iplist:
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[3]

            judge_re = self.judge_ip(ip, port, proxy_type,iplist)
            if judge_re:
                return "{}://{0}:{1}".format(proxy_type, ip, port)
            else:
                return self.get_random_ip()
