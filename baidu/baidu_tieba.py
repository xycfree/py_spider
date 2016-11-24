#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/24 14:45
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
from sogou import sogou
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Baidu_tieba(sogou.Sogou):
    def __init__(self):
        super(Baidu_tieba, self).__init__()
        self.data = {
            'isnew': 1,
            'kw': '',
            'rn': 10,
            'un': '',
            'only_thread': 0,
            'sm': 1,
            'sd': '',
            'ed': '',
            'ie': 'utf-8',
            #'pn': 4,
            #'qw': '广发银行'
        }

    def get_html_info(self, query, page=1, time=0, startTime='',
                endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), site=(100,)):
        '''
        :param query: 关键词
        :param page: 页数
        :param time: 时间
        :param startTime: 自定义开始时间
        :param endTime: 自定义结束时间
        :param site: 站点
        :return:
        '''
        self.data['qw'] = '' + query + ''
        #self.data['pn'] = page
        try:
            self.soup = self.get_info(self.baidu_tieba_url, **self.data)
            #print(self.soup)
            info_list = []
            tieba = self.soup.find('div', class_="s_post_list")
            info_list = []
            if tieba:
                s_post = tieba.find_all('div', class_='s_post')
                for i in s_post:
                    info = {}
                    if i.find('p', class_="p_hot p_content"):
                        info['keywords'] = query
                        info['url'] = i.find('a', class_="bluelink").get('href')
                        info['title'] = i.find('a', class_="bluelink").get_text()
                        info['intro'] = i.find('p', class_="p_hot p_content").get_text()
                        info['website'] = '百度贴吧'
                        tn = i.find('div', class_="p_show").get_text().split('/')
                        info['tieba_name'] = tn[0].strip()
                        info['time'] = tn[1].strip()
                    elif i.find('div', attrs={'id':"no_head",'class':"s_post p_title  post_user clearfix"}):
                        continue
                    else:
                        info['keywords'] = query
                        print('hello')
                        info['url'] = i.find('a', class_="bluelink").get('href')
                        print(info['url'])
                        info['title'] = i.find('a', class_="bluelink").get_text()
                        print(info['title'])
                        info['intro'] = i.find('div', class_="p_content").get_text()
                        print(info['intro'])
                        info['website'] = '百度贴吧'
                        info['tieba_name'] = i.find('a', class_="p_forum")#.find('font', class_="p_violet").get_text()
                        print(info['tieba_name'])
                    #print(info)




            else:
                pass



            return 'true'

        except Exception, e:
            return str(e)
if __name__ == '__main__':
    query = '广发银行'
    page = 2
    tieba = Baidu_tieba()
    result = tieba.get_html_info(query, page)
    print(result)







