#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/23 14:05
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import tornado.httpserver
from tornado import ioloop, web
import tornado.options
from tornado.options import options, define
from sogou import sogou_weixin, sogou_zhihu
from baidu import baidu_news, baidu_tieba
import json
import re
import threading

define('port', default=8000, type=int)

results = {}

class IndexHandlers(tornado.web.RequestHandler):
    def get(self):
        self.args = self.get_argument('name', '品尚')

        self.write('hello tornado!')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.query = self.get_argument('query', '启迪金控')
        self.page = self.get_argument('page', '1')
        self.time_type = self.get_argument('time_type', '0')
        self.site = self.get_argument('site', ('100'))

        # threads = []
        #
        # wx = threading.Thread(target=self.get_wx_info, args=(
        #         self.query,self.page,self.time_type,self.site))
        # zh = threading.Thread(target=self.get_zh_info, args=(
        #         self.query,self.page,self.time_type,self.site))
        # news = threading.Thread(target=self.get_bd_news_info, args=(
        #         self.query,self.page,self.time_type,self.site))
        # tieba = threading.Thread(target=self.get_bd_tieba_info, args=(
        #         self.query,self.page,self.time_type,self.site))
        # threads += [wx,zh,news,tieba]
        # for t in threads:
        #     t.start()

        t = Th(self.query, self.page, self.time_type, self.site)
        t.start()
        print(t.name)


        # wx = self.get_wx_info(self.query, self.page, self.time_type, self.site)
        # zh = self.get_zh_info(self.query, self.page, self.time_type, self.site)
        # news = self.get_bd_news_info(self.query, self.page, self.time_type, self.site)
        # tieba = self.get_bd_tieba_info(self.query, self.page, self.time_type, self.site)

        # result = {}
        #
        # if wx['code'] == 0 or zh['code'] == 0 or tieba['code']==0 or news['code']==0:
        #
        #     result['code'] = 0
        #     result['msg'] = '成功'
        #     result['data'] = {}
        #     wx_total = int(re.sub(',', '', str(wx['data']['total'])))
        #     zh_total = int(re.sub(',', '', str(zh['data']['total'])))  # re.sub(patten,repl,string,count,flags),
        #     news_total = int(re.sub(',', '', str(news['data']['total'])))
        #     tieba_total = int(re.sub(',', '', str(tieba['data']['total'])))
        #
        #     result['data']['total'] = wx_total + zh_total + news_total + tieba_total
        #     result['data']['result'] = wx['data']['result'] + zh['data']['result'] + news['data']['result'] + tieba['data']['result']
        #
        # else:
        #     result['code'] = 1
        #     result['msg'] = wx['msg']
        #     result['data'] = {}
        #     result['data']['total'] = 0
        #     result['data']['result'] = []
        # # return json.dumps(result)
        # self.write(json.dumps(result))

        self.write(json.dumps(results))






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
        results['wx'] = self.wx
        results['zh'] = self.zh
        results['news'] = self.news
        results['tieba'] = self.tieba

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

if __name__ == "__main__":
    tornado.options.parse_command_line()  # 解析
    app = tornado.web.Application(handlers=[
        (r'/', IndexHandlers),
        (r'/so', MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
