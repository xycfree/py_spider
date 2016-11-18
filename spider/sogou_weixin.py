#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/16 22:48
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os

import MySQLdb
from bs4 import BeautifulSoup
import requests
from db_config import mysql_conn
import sys
from quene import Producer, Consumer
reload(sys)
sys.setdefaultencoding('utf-8')


class Sogou_Wechat(object):
    def __init__(self):
        super(Sogou_Wechat, self).__init__()
        self.base_url = r'https://www.sogou.com/'
        self.wx_url = r'http://weixin.sogou.com/weixin'
        self.data = {
            'type': 2,
            # 'query': "广发银行",
            'ie': 'utf8',
            '_sug_': 'n',
            # 'page': 1,
            '_sug_type_': ''}


    def get_wx_info(self, info, count):
        if info is not None and count is not None:
            self.info = info
            self.count = count
            c = Producer(self.info)
            c.start()
            page = count / 10 + 1 if count % 10 else count / 10
            for i in range(1,page):
                pass


        else:
            print('无数据')


    def get_html_info(self, query, page=1, *args, **kwargs):
        '''
        :param query: 搜索的关键词
        :return: 返回第一页数据，总数据条数
        '''
        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page
        '''限定时间范围
        <a id="left_timespan_4"  href="?query=%22%E8%81%94%E6%8B%93%E5%A4%A9%E9%99%85%22&_sug_type_=
         &_sug_=n&type=2&ie=utf8&sourceid=inttime_year&interation=&interV=kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304&tsn=4">
         一年内</a>
        '''
        # self.data['sourceid'] = 'inttime_year' # 一年内, inttime_all全部
        # self.data['interation'] = ''
        # self.data['interV'] = 'kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304'
        # self.data['tsn'] = 4
        try:
            r = requests.get(self.wx_url, params=self.data, timeout=6).content
            soup = BeautifulSoup(r, 'lxml')
            container = soup.find('body', class_='').find('div', class_="results").find_all('div',
                class_="wx-rb wx-rb3")
            info_list = []
            if container:
                for i in container:
                    info = []
                    info.append(query)
                    info.append(i.find('div', class_='txt-box').find('a').get_text())  # url标题
                    info.append(str(i.find('div', class_="txt-box").find('a').get('href')))  # url
                    info.append(i.find('div', class_='txt-box').find('p').get_text())  # 简介
                    text = self.get_text(i.find('div', class_="txt-box").find('a').get('href'))
                    info.append(text) #详情

                    #多线程
                    self.mysql_insert(info)

                    info_list.append(info)

                pagebar_container = soup.find('div', attrs={'class': "p", 'id': "pagebar_container"})
                count = pagebar_container.find('div', class_='mun').find('resnum',
                    attrs={'id': 'scd_num'}).get_text().strip()

            else:
                return None, None
            return info_list, count
        except Exception, e:
            return str(e)

    def get_text(self,url):
        '''
        :param url: 访问的url地址
        :return: 获取text内容
        '''
        r = requests.get(url).content
        soup = BeautifulSoup(r,'lxml')
        text = soup.find('div', attrs={'class':"rich_media_content ",'id':"js_content"}).get_text()
        return text

    def mysql_insert(self, info):

        #conn = MySQLdb.connect(host="127.0.0.1",port=3306, user="root", passwd="root", db="jfpython", charset="utf8")
        #cursor = conn.cursor()
        # result = cursor.execute("INSERT INTO craw_data(keywords,title,url,intro,details) VALUES('aa','33','333','adsf','safd');")
        # conn.commit()

        print(len(info[2]))
        #print('{0},{1},{2},{3},{4}'.format(info[0],info[1],info[2],info[3],info[4]))
        query = '''INSERT INTO craw_data(keywords,title,url,intro,details)
                      VALUES ("{k}", "{t}", "{u}", "{i}", "{d}");
                '''.format(k=info[0], t=info[1], u=info[2], i=info[3], d=info[4])
        mysql = mysql_conn.Mysql()
        result = mysql.insert_one(query)
        return result




if __name__ == '__main__':
    sogou = Sogou_Wechat()
    key_words = '联拓天际'
    print(sogou.get_html_info(key_words))
    #print(info, count)

    #sogou.get_wx_info(info, count)

    #sogou.get_text('http://mp.weixin.qq.com/s?src=3&timestamp=1479433045&ver=1&signature=ux*HwkgtrUXLWRypB*SidzqK*7*aR9sM5fK4j9CGaWz38kJ5PRuayRAysgJ1DmU0QznsvJ7AO5lwnwxOO0LndGCVPQpdy93v3GCns5h2LyVJ8Hg-T6npp5UyViYAjnyILNA8K0f3N-sC6Fw16wtpdPi5UqDFjAg6PyQsiI6T1C8=')

