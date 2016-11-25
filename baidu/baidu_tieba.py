#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/24 14:45
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os

import re

from sogou import sogou
import datetime
import json
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
            # 'pn': 4,
            # 'qw': '广发银行'
        }

    def get_html_info(self, query, page=1, time_type=0, startTime='',
                endTime=datetime.datetime.now().strftime('%Y-%m-%d'), site=(100,)):
        '''
        :param query: 关键词
        :param page: 页数
        :param time_type: 时间
        :param startTime: 自定义开始时间
        :param endTime: 自定义结束时间
        :param site: 站点
        :return:
        '''
        self.data['qw'] = '' + query + ''
        self.data['pn'] = page
        try:
            self.soup = self.get_info(self.baidu_tieba_url, **self.data)
            info_list = []
            tieba = self.soup.find('div', class_="s_post_list")
            if tieba:
                s_post = tieba.find_all('div', class_='s_post')
                for i in s_post:
                    info = {}
                    if i.get('class')[0] == 's_post' and len(i.get('class')) != 1:
                        continue
                    if i.find('p', class_="p_hot p_content"):
                        info['keywords'] = query
                        info['url'] = i.find('a', class_="bluelink").get('href')
                        info['title'] = i.find('a', class_="bluelink").get_text()
                        info['intro'] = i.find('p', class_="p_hot p_content").get_text()
                        info['website'] = '百度贴吧'
                        tn = i.find('div', class_="p_show").get_text().split('/')
                        info['tieba_name'] = tn[0].strip()
                        info['time'] = tn[1].strip()
                    else:
                        info['keywords'] = query
                        t_url = i.find('a', class_="bluelink").get('href')
                        info['url'] = self.tieba_base + t_url if self.tieba_base not in t_url else t_url
                        info['title'] = i.find('a', class_="bluelink").get_text()
                        info['intro'] = i.find('div', class_="p_content").get_text()
                        info['website'] = '百度贴吧'
                        info['tieba_name'] = i.find_all('font', class_="p_violet")[0].get_text()
                        info['author'] = i.find_all('font', class_="p_violet")[1].get_text()
                        info['time'] = i.find('font', class_="p_green p_date").get_text()
                    info_list.append(info)

            counts = self.soup.find('span', class_='s_nav_right hasPage')
            count = counts.get_text().split('，')[1][8:-1] if counts else 0
            # class ="s_nav_right hasPage" > 百度一下，找到相关贴吧贴子177407篇，用时0.417秒
            result = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'total': count,
                    'result': info_list
                }
            }

            return json.dumps(result, indent=1)

        except Exception, e:
            result = {
                'code': 1,
                'msg': str(e),
                'data': {
                    'total': 0,
                    'result': []
                }
            }
            return json.dumps(result, indent=1)


if __name__ == '__main__':
    query = '张家口'
    page = 1

    tieba = Baidu_tieba()
    result = tieba.get_html_info(query, page)
    print(result)
