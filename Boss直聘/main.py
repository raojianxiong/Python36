# -*- coding:utf-8 _*-  
""" 
@author:Jianxiong Rao 
@file: main.py 
@time: 2018/05/16 
"""
from scrapy.cmdline import execute
import sys
import os

# 获取当前运行脚本的绝对路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", 'crawl', 'boss'])
