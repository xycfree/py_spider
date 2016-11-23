#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-06 21:53:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $

import os
import tornado.httpserver
from tornado import ioloop,web
import tornado.options
from tornado.options import options,define
from lagou_info import Lagou_info
from job51 import Job51_info
from sogou import sogou_weixin,sogou_zhihu
import json

define('port', default=8000, type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        '''curl http://localhost:8000/?greeting=Salutations
        :return:
        '''

        self.write("Hello, world ")
        self.company_name = self.get_argument('companyName', '品尚')
        lagou = Lagou_info()
        self.url = lagou.get_company_url(self.company_name)
        self.soup, self.company_id, self.comp_data = lagou.get_company_info(self.url)
        self.basic_info = lagou.get_comp_basic_info(self.soup)
        for key in self.basic_info.keys():
            self.write('{0} : {1} '.format(key,self.basic_info[key]))



class IndexHandlers(tornado.web.RequestHandler):
    def get(self):
        args = self.get_argument('name','品尚')
        job51 = Job51_info()
        comp_info = job51.get_company_info(args)
        comp_posi_info = job51.get_comp_position_info(comp_info, args)
        if comp_posi_info['posi_list']:
            for key,value in comp_posi_info.items():
                if key != 'posi_list':
                    self.write('{0} : {1} \n'.format(key,value))
                else:
                    lines = len(value) #职位条数
                    keys = value[0] # 字段数
                    # for j in value:
                    #     print('列')
                    for i in value:
                        print('字段')
                        self.write('{0},{1},{2},{3},{4},{5} \n'.format(i[0],i[1],i[2],i[3],i[4],i[5]))
        else:
            self.write(args + 'success')

# application = tornado.web.Application([
#     (r"/",MainHandler),
# ])

class WechatHandler(tornado.web.RequestHandler):
    def get(self):
        self.query = self.get_argument('query', '启迪金控')
        self.page = self.get_argument('page', '1')
        self.time = self.get_argument('time', '0')
        self.site = self.get_argument('site', ('100'))
        self.wx = sogou_weixin.Sogou_Wechat()
        result = self.wx.get_html_info(self.query, self.page, self.time, self.site)
        self.write(result)

        # result = json.loads(result)
        #
        # for i in result:
        #     #print(isinstance(i, dict))
        #     #print(type(i))
        #     if isinstance(i, dict):
        #         for k, v in i.items():
        #             self.write('{0} : {1} \n'.format(k, v))
        #     else:
        #         self.write(i)

class ZhihuHandler(tornado.web.RequestHandler):
    def get(self):
        self.query = self.get_argument('query', '启迪金控')
        self.page = self.get_argument('page', '1')
        self.time = self.get_argument('time', '0')
        self.site = self.get_argument('site', ('100'))
        self.zhihu = sogou_zhihu.Sogou_zhihu()
        result = self.zhihu.get_html_info(self.query, self.page, self.time, self.site)
        self.write(result)



if __name__ == "__main__":
    tornado.options.parse_command_line() #解析
    app = tornado.web.Application(handlers=[(r'/', MainHandler),
                                            (r'/comp', IndexHandlers),
                                            (r'/wx', WechatHandler),
                                            (r'/zhihu',ZhihuHandler)
                                            ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    #application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


