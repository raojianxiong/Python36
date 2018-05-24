# -*- coding:utf-8 _*-  
""" 
@author:Jianxiong Rao 
@file: main.py 
@time: 2018/04/01 
"""

from scrapy.cmdline import execute

import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "lagou"])
