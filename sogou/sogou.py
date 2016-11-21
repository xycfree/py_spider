#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/20 23:31
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Sogou(object):
    def __init__(self):
        self.base_url = r'https://www.sogou.com/' # 搜狗
        self.wx_url = r'http://weixin.sogou.com/weixin' # 微信
        self.news_url = r'http://news.sogou.com/'   # 新闻
        self.zhihu_url = r'http://zhihu.sogou.com/zhihu' # 知乎

    def get_info(self,url=None, *args, **kwargs):
        r = requests.get(url, params=kwargs, timeout=6).content
        soup = BeautifulSoup(r, 'lxml')
        return soup