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
import json
import re
import th
from th import Th

define('port', default=8000, type=int)


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
        print('thread start ....')
        t = Th(self.query, self.page, self.time_type, self.site)
        t.setDaemon(True)
        t.start()
        res = th.results
        print(len(res))
        print(json.dumps(res, indent=1))
        #t.cls()
        results = {}
        if len(res):
            if res[0]['code'] == 0 or res[1]['code'] == 0 or res[2]['code'] == 0 or res[3]['code'] == 0:
                results['code'] = 0
                results['msg'] = '成功'
                results['data'] = {}
                results['data']['total'] = 0
                results['data']['result'] = []
                for i in res:
                    results['data']['total'] += int(re.sub(',', '', str(i['data']['total'])))
                    results['data']['result'] += i['data']['result']
            else:
                results['code'] = 1
                results['msg'] = res[0]['msg']
                results['data'] = {}
                results['data']['total'] = 0
                results['data']['result'] = []

        else:
            results['code'] = 0
            results['msg'] = '成功'
            results['data'] = {}
            results['data']['total'] = 0
            results['data']['result'] = []
        # th.res = []
        # th.results = []

        self.write(json.dumps(results))

        # return json.dumps(results, indent=1)


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


if __name__ == "__main__":
    tornado.options.parse_command_line()  # 解析
    app = tornado.web.Application(handlers=[
        (r'/', IndexHandlers),
        (r'/so', MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
