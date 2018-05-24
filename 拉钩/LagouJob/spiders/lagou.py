# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LagouJob.utils.common import extract_num
from LagouJob.items import LagouJobItemLoader, LagoujobItem
from datetime import datetime
import random
from selenium import webdriver
from LagouJob.settings import user_agent_list
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class LagouJobSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    # 换了好几种做法，最后是自己登陆网站，将Cookie换成自己登录后的Cookie，能爬取更多，否则只能5页左右吧
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': ' * / * ',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'HMACCOUNT=A260CBB990D0DB84; BAIDUID=3BB23B14A56AD042655176A6FBE62DAD:FG=1; BIDUPSID=CAEA0B205688B3652CCA0D366D56FAB8; PSTM=1525050093; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDUSS=J6U29hTVdNT2pocEJLYkZvbDllRzUyeERXRTlFalk4d2Z1SG5oT1NkVXE1eXRiQVFBQUFBJCQAAAAAAAAAAAEAAAAbjNdHsK7QprXEuaS088POAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACpaBFsqWgRbWG; H_PS_PSSID=; PSINO=1; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1527164947|',
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
    }
    rules = (
        Rule(LinkExtractor(allow=r'https://www.lagou.com/jobs/\d+.html'), callback='parse_job', follow=True),
    )

    # # 动态设置User_Agent
    # random_index = random.randint(0, len(user_agent_list))
    # random_agent = user_agent_list[random_index]

    # 以下是关闭浏览器
    # def __init__(self):
    #     self.browser = webdriver.Firefox()  # executable_path=""
    #     super().__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     self.browser.quit()

    def parse_job(self, response):
        print("开始解析")
        item_loader = LagouJobItemLoader(item=LagoujobItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value("job_id", extract_num(response.url))
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath("work_years", '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath("degree_need", '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath("job_type", '//*[@class="job_request"]/p/span[5]/text()')

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_value("crawl_time", datetime.now())

        item = item_loader.load_item()
        return item
