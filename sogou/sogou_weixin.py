#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/16 22:48
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import datetime
import json
import sys
import time

import re

from py_spider.config.db_config import mysql_conn
from py_spider.config.log_info import Logger
from sogou import Sogou

# from queue import Consumer, Producer
reload(sys)
sys.setdefaultencoding('utf-8')
logger = Logger()


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
                      endTime=datetime.datetime.now().strftime('%Y-%m-%d'), site=(100,)):
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

        # self.data['query'] = si + '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page
        # if time_type in self.tsn:
        #     if time_type != 0:
        #         self.data['sourceid'] = self.sourceid[-time_type]  # 一年内, inttime_all全部
        #         self.data['interation'] = ''
        #         self.data['interV'] = 'kKIOkrELjboJmLkElbYTkKIKmbELjbkRmLkElbk%3D_1893302304'
        #         self.data['tsn'] = self.tsn[-time_type]
        # else:
        #     # startTime
        #     # endTime
        #     pass  # 自定义 默认为全部

        try:

            soup = self.get_info(self.wx_url, **self.data)
            container = soup.find('ul', class_="news-list")

            json_info = []
            if container:
                logger.info('请求信息正确，返回信息成功！')
                for i in container.find_all('div', class_="txt-box"):
                    jso = {}
                    jso['keywords'] = query
                    jso['title'] = i.find('a').get_text()
                    print(jso['title'])

                    jso['url'] = i.find('a').get('href').encode('utf-8')
                    print(jso['url'])

                    jso['intro'] = i.find('p', class_="txt-info").get_text() if i.find(
                        'p', class_="txt-info") else "暂无"
                    print(jso['intro'])

                    jso['website'] = '微信'
                    jso['wechat_name'] = i.find('a', class_="account").get_text()
                    print(jso['wechat_name'])

                    t = i.find('span', class_="s2").get_text()[-13:-3].encode('utf-8')
                    stamp = time.localtime(float(t))  # 时间戳转换为本地时间
                    jso['time'] = time.strftime('%Y-%m-%d', stamp)  # time.strftime('%Y-%m-%d %H:%M:%S',x)
                    print(jso['time'])

                    jso['read'] = i.find('span', class_='s1').get_text()  # 阅读人数
                    print(jso['read'])

                    # 点赞人数，获取不到，是动态数据

                    text = self.get_text_info(jso['url'])
                    jso['details'] = text  # 详情
                    print(jso['details'])
                    json_info.append(jso)

                    # 多线程
                    # result = self.mysql_insert(info)
            count = soup.find('div', class_="mun").get_text()[3:-3] if soup.find('div', class_="mun") else 0  # 总条数
            result = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'total': count,
                    'result': json_info
                }
            }
            return json.dumps(result, indent=1, ensure_ascii=False)  # 字典转换为json，并格式化
        except Exception, e:
            logger.error('异常信息:{}'.format(e))
            result = {
                'code': 1,
                'msg': str(e),
                'data': {
                    'total': 0,
                    'result': []
                }
            }
            return json.dumps(result, indent=1, ensure_ascii=False)

    def get_text_info(self, url):
        '''
        :param url: 访问的url地址
        :return: 获取text内容
        '''
        logger.info('请求get_text_info方法,')
        soup = self.get_info(url)
        text = soup.find('div', attrs={'class': "rich_media_content ", 'id': "js_content"}).get_text()
        text = re.sub(re.compile('\n| '), '', text).strip()
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
    key_words = '品尚'
    page = 1
    time_type = 2
    site = ('101', '102')
    result = sogou.get_html_info(query=key_words, page=page)
    print(result)
