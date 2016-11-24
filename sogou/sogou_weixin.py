#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/16 22:48
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

from db_config import mysql_conn
import sys
from sogou import Sogou
import json
import datetime
import time

# from queue import Consumer, Producer
reload(sys)
sys.setdefaultencoding('utf-8')


class Sogou_Wechat(Sogou):
    def __init__(self):
        super(Sogou_Wechat, self).__init__()

        self.data = {
            'type': 2,
            # 'query': "广发银行",
            'ie': 'utf8',
            '_sug_': 'n',
            # 'page': 1,
            '_sug_type_': ''}

    def get_wx_info(self, info, count):
        if count and info:
            self.info = info
            self.count = count
            page = count / 10 + 1 if count % 10 else count / 10
            for i in range(2, page + 1):
                pass
        else:
            print('无数据')

    def get_html_info(self, query, page=1, time_type=0, startTime='',
            endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), site=(100,)):
        '''
        :param query: 查询关坚持
        :param page: 页数
        :param time_type: 查询的时间段
        :param site: 来源，站点
        :return:
        '''
        si = ''
        for i in site:
            if i in self.site_type.keys():
                si += self.site_type[i] + '|'
        si = si[:-1] if si else ''

        #self.data['query'] = si + '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page
        if time_type in self.tsn:
            if time_type != 0:
                self.data['sourceid'] = self.sourceid[-time_type]  # 一年内, inttime_all全部
                self.data['interation'] = ''
                self.data['interV'] = 'kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304'
                self.data['tsn'] = self.tsn[-time_type]
        else:
            # startTime
            # endTime
            pass  # 自定义 默认为全部
        try:
            soup = self.get_info(self.wx_url, **self.data)
            container = soup.find('body', class_='').find('div', class_="results").find_all('div',
                                                                                            class_="wx-rb wx-rb3")
            json_info = []
            if container:
                for i in container:
                    jso = {}
                    jso['keywords'] = query
                    jso['title'] = i.find('div', class_='txt-box').find('a').get_text()
                    jso['url'] = i.find('div', class_="txt-box").find('a').get('href').encode('utf-8')
                    jso['intro'] = i.find('div', class_='txt-box').find('p').get_text()
                    jso['website'] = i.find('div', class_="txt-box").find('a', class_="wx-name").get('title')
                    t = i.find('div', class_="txt-box").find('span', class_="time").find(
                        'script').get_text()[-12:-2] .encode('utf-8')
                    stamp = time.localtime(float(t)) # 时间戳转换为本地时间
                    jso['time'] = time.strftime('%Y-%m-%d', stamp) # time.strftime('%Y-%m-%d %H:%M:%S',x)
                    # text = self.get_text(i.find('div', class_="txt-box").find('a').get('href'))
                    # jso['details'] = text # 详情
                    json_info.append(jso)

                    # info = []
                    # info.append(query)
                    # info.append(i.find('div', class_='txt-box').find('a').get_text())  # url标题
                    # info.append(str(i.find('div', class_="txt-box").find('a').get('href')))  # url
                    # info.append(i.find('div', class_='txt-box').find('p').get_text())  # 简介
                    # text = self.get_text(i.find('div', class_="txt-box").find('a').get('href'))
                    # info.append(text) #详情
                    # print(json_info)

                    # 多线程
                    # result = self.mysql_insert(info)

                pagebar_container = soup.find('div', attrs={'class': "p", 'id': "pagebar_container"})
                count = pagebar_container.find('div', class_='mun').find('resnum',
                                                                         attrs={
                                                                             'id': 'scd_num'}).get_text().strip()  # 总条数

            else:
                json_info = []
                count = 0

            #json_info = json.dumps(json_info, indent=1)
            result = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'total': count,
                    'result': json_info
                }
            }
            return json.dumps(result, indent=1)   # count, json.dumps(json_info, indent=1)  # 字典转换为json，并格式化
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

    def get_text(self, url):
        '''
        :param url: 访问的url地址
        :return: 获取text内容
        '''
        soup = self.get_info(url)
        text = soup.find('div', attrs={'class': "rich_media_content ", 'id': "js_content"}).get_text()
        return text

    def mysql_insert(self, info):
        '''

        :param info: 写入数据库信息
        :return: 返回id
        '''
        query = '''INSERT INTO craw_data(keywords,title,url,intro,details)
                      VALUES ("{k}", "{t}", "{u}", "{i}", "{d}");
                '''.format(k=info[0], t=info[1], u=info[2], i=info[3], d=info[4])
        mysql = mysql_conn.Mysql()
        result = mysql.insert_one(query)
        return result


if __name__ == '__main__':
    sogou = Sogou_Wechat()
    key_words = '联拓天际'

    page = 5
    time_type = 2
    site = ('101', '102')
    result = sogou.get_html_info(query=key_words, page=page)
    #result = json.loads(result) # json转换为字典
    #print(result['data']['total'])
    print(result)
