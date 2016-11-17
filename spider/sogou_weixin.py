#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/16 22:48
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
from bs4 import BeautifulSoup
import requests
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Sogou_Wechat(threading.Thread):
    def __init__(self):
        super(Sogou_Wechat, self).__init__()
        self.base_url = r'https://www.sogou.com/'
        self.wx_url = r'http://weixin.sogou.com/weixin'

    def run(self):
        pass

    def get_wx_info(self):
        pass

    def get_html_info(self, query):
        data = {
            'type': 2,
            # 'query': "广发银行",
            'ie': 'utf8',
            '_sug_': 'n',
            # 'page': 1,
            '_sug_type_': ''
        }
        data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        '''限定时间范围
        <a id="left_timespan_4"  href="?query=%22%E8%81%94%E6%8B%93%E5%A4%A9%E9%99%85%22&_sug_type_=
         &_sug_=n&type=2&ie=utf8&sourceid=inttime_year&interation=&interV=kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304&tsn=4">
         一年内</a>
        '''
        # self.data['sourceid'] = 'inttime_year' # 一年内, inttime_all全部
        # self.data['interation'] = ''
        # self.data['interV'] = 'kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304'
        # self.data['tsn'] = 4

        r = requests.get(self.wx_url, params=data, timeout=6).content
        soup = BeautifulSoup(r, 'lxml')
        container = soup.find('body', class_='').find('div', class_="results").find_all('div', class_="wx-rb wx-rb3")
        info_list = []
        if container:
            for i in container:
                info = []
                info.append(i.find('div', class_="txt-box").find('a').get('href'))  # url
                info.append(i.find('div', class_='txt-box').find('a').get_text()) # url标题
                info.append(i.find('div', class_='txt-box').find('p').get_text()) # 简介
                info_list.append(info)
                print('{0},{1},{2}'.format(info[0],info[1],info[2]))
            print(info_list)

            pagebar_container = soup.find('div', attrs={'class': "p", 'id': "pagebar_container"})
            # print(container)
            # print(pagebar_container)
        else:
            print('没有查询到该信息')


if __name__ == '__main__':
    sogou = Sogou_Wechat()
    sogou.get_html_info("联拓天际")
