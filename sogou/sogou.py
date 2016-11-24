#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/20 23:31
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import requests
from bs4 import BeautifulSoup
from config import UserAgent
from random import randint
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Sogou(object):
    def __init__(self):
        self.base_url = r'https://www.sogou.com/'  # 搜狗
        self.wx_url = r'http://weixin.sogou.com/weixin'  # 微信
        self.news_url = r'http://news.sogou.com/'  # 新闻
        self.zhihu_url = r'http://zhihu.sogou.com/zhihu'  # 知乎
        self.baidu_news_url = r'http://news.baidu.com/ns'  # 百度信息
        self.baidu_tieba_url = r'http://tieba.baidu.com/f/search/res'  # 百度贴吧，全吧搜索
        self.sourceid = ('inttime_all', 'inttime_day', 'inttime_week', 'inttime_month', 'inttime_year')
        self.tsn = (0, 1, 2, 3, 4)
        self.site_type = {
            '100': '',
            '101': 'site:sohu.com ',
            '102': 'site:qq.com ',
            '103': 'site:sina.com.cn ',
            '104': 'site:ifeng.com ',
            '105': 'site:163.com '
        }
        self.site = {'搜狐': 'site:sohu.com ',
                     '腾讯': 'site:qq.com ',
                     '新浪': 'site:sina.com.cn ',
                     '凤凰': 'site:ifeng.com ',
                     '网易': 'site:163.com '
                     }

        ua = len(UserAgent)
        user_agent = UserAgent[randint(1, ua - 1)]
        # print(user_agent)
        self.headers = {
            'User-Agent': user_agent
        }

    def get_info(self, url=None, *args, **kwargs):
        s = requests.session()
        r = s.get(url, params=kwargs, headers=self.headers, timeout=10).content
        soup = BeautifulSoup(r, 'lxml')
        return soup


if __name__ == '__main__':
    sogou = Sogou()
