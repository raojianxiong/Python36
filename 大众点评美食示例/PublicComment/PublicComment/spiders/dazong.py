# -*- coding: utf-8 -*-
import scrapy
from PublicComment.items import PublicspiderItem, PubliccommentItem
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class DazongSpider(scrapy.Spider):
    name = 'dazong'
    allowed_domains = ['dianping.com']
    start_urls = ["http://www.dianping.com/tianjin/ch10"]
    for i in range(2, 51):
        start_urls.append("http://www.dianping.com/tianjin/ch10/p{}".format(i))
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'Cookie': '_lx_utm = utm_source % 3DBaidu % 26utm_medium % 3Dorganic;_lxsdk_cuid = 162f7ee076bc8 - 0b897028c7bbd - d35346d - 144000 - 162f7ee076cc8;_lxsdk = 162f7ee076bc8 - 0b897028c7bbd - d35346d - 144000 - 162f7ee076cc8;_hc.v = 098800ce - eb26 - f811 - bf59 - f7f9a68c3089.1524577995;cy = 10;cye = tianjin;s_ViewType = 10',
            'Host': 'www.dianping.com',
            'Referer': 'http: // www.dianping.com / shopall / 10 / 0',

            'Referer': 'http://www.dianping.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    def __init__(self):
        # self.browser = webdriver.PhantomJS(executable_path="D://Program Files//Phantomjs//phantomjs-2.1.1-windows//bin\phantomjs.exe")  # executable_path=""
        self.browser = webdriver.Firefox()
        super().__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.browser.get("http://www.dianping.com/tianjin")
        import time
        time.sleep(2)
        self.browser.find_element_by_css_selector(
            "#cata-hot > div.cata-hot-detail.cata-hot-info > div > a").click()
        self.browser.find_element_by_css_selector("#logo-input > div > a.city.J-city > i").click()
        time.sleep(10)

    def spider_closed(self):
        self.browser.quit()
        self.browser.close()

    def parse(self, response):
        print(response.text)

        lis = response.css("#shop-all-list ul li")
        # print(len(lis))
        for node in lis:
            name = node.css("div.tit a h4::text").extract_first()
            start = node.css("div.comment > span::attr(title)").extract_first()
            taste = node.css("div.txt span.comment-list span:nth-child(1) b::text").extract_first()
            environment = node.css("div.txt span.comment-list span:nth-child(2) b::text").extract_first()
            service = node.css("div.txt span.comment-list span:nth-child(3) b::text").extract_first()
            tag = node.css("div.tag-addr a:nth-child(1) span::text").extract_first()
            comments = node.css("div.comment a.review-num > b::text").extract_first()
            price = node.css("div.comment a.mean-price > b::text").extract_first()
            area = node.css("div.tag-addr a:nth-child(3) span::text").extract_first()
            address = node.css("div.tag-addr > span::text").extract_first()
            recommend_food = node.css("div.recommend a::text").extract()
            has_bulk = node.css("div.svr-info a:nth-child(1)::attr(title)").extract_first()
            preferential = node.css("div.svr-info a.tuan.privilege::text").extract_first()
            link = node.css("div.tit > div a:nth-child(1)::attr(href)").extract_first()

            item = PubliccommentItem()
            item['name'] = name if name is not None else ""
            item['start'] = start if start is not None else ""
            item['taste'] = taste if taste is not None else ""
            item['environment'] = environment if environment is not None else ""
            item['service'] = service if service is not None else ""
            item['tag'] = tag if tag is not None else ""
            item['comments'] = comments if comments is not None else ""
            item['price'] = price if price is not None else "暂无"
            item['area'] = area if area is not None else ""
            item['address'] = address if address is not None else ""
            item['recommend_food'] = "  ".join(recommend_food) if recommend_food is not None else "暂无"
            item['has_bulk'] = has_bulk if has_bulk is not None else "暂无"
            item['preferential'] = preferential if preferential is not None else "暂无"
            item['link'] = link if link is not None else ""

            yield item
        # for i in range(1, len(lis) + 1):
        #     item_loader = PublicspiderItem(item=PubliccommentItem(), response=response)
        #     item_loader.add_css("name", "#shop-all-list ul li:nth-child({}) div.tit a h4::text".format(i))
        #     item_loader.add_css("start", "#shop-all-list ul li:nth-child({}) div.comment > span::attr(title)".format(i))
        #     item_loader.add_css("taste",
        #                         "#shop-all-list ul li:nth-child({}) div.txt span.comment-list span:nth-child(1) b::text".format(
        #                             i))
        #     item_loader.add_css("environment",
        #                         "#shop-all-list ul li:nth-child({}) div.txt span.comment-list span:nth-child(2) b::text".format(
        #                             i))
        #     item_loader.add_css("service",
        #                         "#shop-all-list ul li:nth-child({}) div.txt span.comment-list span:nth-child(3) b::text".format(
        #                             i))
        #     item_loader.add_css("tag",
        #                         "#shop-all-list ul li:nth-child({}) div.tag-addr a:nth-child(1) span::text".format(i))
        #     item_loader.add_css("comments",
        #                         "#shop-all-list ul li:nth-child({}) div.comment a.review-num > b::text".format(i))
        #     item_loader.add_css("price",
        #                         "#shop-all-list ul li:nth-child({}) div.comment a.mean-price > b::text".format(i))
        #     item_loader.add_css("area",
        #                         "#shop-all-list ul li:nth-child({}) div.tag-addr a:nth-child(3) span::text".format(i))
        #     item_loader.add_css("address", "#shop-all-list ul li:nth-child({}) div.tag-addr > span::text".format(i))
        #     item_loader.add_css("recommend_food", "#shop-all-list ul li:nth-child({}) div.recommend a::text".format(i))
        #     item_loader.add_css("has_bulk",
        #                         "#shop-all-list ul li:nth-child({}) div.svr-info a:nth-child(1)::text".format(i))
        #     item_loader.add_css("preferential",
        #                         "#shop-all-list ul li:nth-child({}) div.svr-info a.tuan.privilege::text".format(i))
        #     item_loader.add_css("link",
        #                         "#shop-all-list ul li:nth-child({}) div.tit > div a:nth-child(1)::attr(href)".format(i))
        #     item = item_loader.load_item()

            # yield item
