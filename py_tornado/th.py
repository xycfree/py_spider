#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/25 17:30
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import threading
import json

from sogou import sogou_weixin, sogou_zhihu
from baidu import baidu_news, baidu_tieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Th(threading.Thread):

    def __init__(self,query,page=1,time_type=0,site=(100,)):
        super(Th,self).__init__()
        self.query = query
        self.page = page
        self.time_type = time_type
        self.site = site

        self.wx = self.get_wx_info(self.query, self.page, self.time_type, self.site)
        self.zh = self.get_zh_info(self.query, self.page, self.time_type, self.site)
        self.news = self.get_bd_news_info(self.query, self.page, self.time_type, self.site)
        self.tieba = self.get_bd_tieba_info(self.query, self.page, self.time_type, self.site)

    def run(self):
        global results
        results = []
        results.append(self.wx)
        results.append(self.zh)
        results.append(self.news)
        results.append(self.tieba)

    #print('results:{}'.format(results))
    #res = results
    #results = []

    def stop(self):
        self.stopped = True

    def cls(self):
        results = []

    def get_wx_info(self, query, page, time_type, site):
        self.weixin = sogou_weixin.Sogou_Wechat()
        result = json.loads(self.weixin.get_html_info(query, page, time_type, site))
        return result

    def get_zh_info(self, query, page, time_type, site):
        self.zhihu = sogou_zhihu.Sogou_zhihu()
        result = json.loads(self.zhihu.get_html_info(query, page, time_type, site))
        return result

    def get_bd_news_info(self, query, page, time_type, site):
        self.news = baidu_news.Baidu_news()
        result = json.loads(self.news.get_html_info(query, page, time_type, site))
        return result

    def get_bd_tieba_info(self, query, page, time_type, site):
        self.tieba = baidu_tieba.Baidu_tieba()
        result = json.loads(self.tieba.get_html_info(query, page, time_type, site))
        return result

if __name__ == '__main__':
    t = Th(3, 5, 2)
    t.start()
    print(results)
