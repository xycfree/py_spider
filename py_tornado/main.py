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
import json
import re

define('port', default=8000, type=int)

class IndexHandlers(tornado.web.RequestHandler):
    def get(self):
        self.args = self.get_argument('name','品尚')

        self.write('hello tornado!')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.query = self.get_argument('query', '启迪金控')
        self.page = self.get_argument('page', '1')
        self.time = self.get_argument('time', '0')
        self.site = self.get_argument('site', ('100'))

        self.weixin = sogou_weixin.Sogou_Wechat()
        wx = json.loads(self.weixin.get_html_info(self.query, self.page, self.time, self.site))

        self.zhihu = sogou_zhihu.Sogou_zhihu()
        zh = json.loads(self.zhihu.get_html_info(self.query, self.page, self.time, self.site))
        result = {}
        print(int(re.sub(',', '', str(wx['data']['total']))))
        print(int(re.sub(',', '', str(zh['data']['total']))))
        if wx['code'] == 0 or zh['code'] == 0:

            result['code'] = 0
            result['msg'] = '成功'
            result['data'] = {}
            wx_total = int(re.sub(',', '', str(wx['data']['total'])))
            zh_total = int(re.sub(',', '', str(zh['data']['total']))) #re.sub(patten,repl,string,count,flags),
            result['data']['total'] = wx_total + zh_total
            result['data']['result'] = wx['data']['result'] + zh['data']['result']
        else:
            result['code'] = 1
            result['msg'] = wx['msg']
            result['data'] = {}
            result['data']['total'] = 0
            result['data']['result'] = []
        # return json.dumps(result)
        self.write(json.dumps(result))


if __name__ == "__main__":
    tornado.options.parse_command_line()  # 解析
    app = tornado.web.Application(handlers=[
        (r'/', IndexHandlers),
        (r'/so', MainHandler),
        ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
