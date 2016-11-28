#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/22 9:55
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import datetime
from sogou import Sogou
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Sogou_zhihu(Sogou):
    def __init__(self):
        super(Sogou_zhihu, self).__init__()
        self.data = {
            'ie': 'utf-8'
        }

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

        self.data['query'] = '"' + str(query) + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = int(page)

        try:
            soup = self.get_info(self.zhihu_url, **self.data)
            box_result = soup.find('div', class_='zhihu-warp').find('div', class_='result-content').find('div',
                                                                                                         class_="box-result")
            json_info = []
            if box_result:
                content_result = soup.find('div', class_='box-result').find_all('div', class_='result-about-list')
                for i in content_result:
                    jso = {}
                    jso['keywords'] = query
                    jso['title'] = i.find('h4', class_='about-list-title').find('a').get_text()
                    jso['url'] = i.find('h4', class_="about-list-title").find('a').get('href')
                    jso['intro'] = ''
                    jso['website'] = '知乎'
                    jso['time'] = ''
                    # print('{0},{1},{2}'.format(jso['title'],jso['url'],jso['intro']))
                    # text = self.get_text(i.find('h4', class_="about-list-title").find('a').get('href'))
                    # jso['details'] = text # 内容详情
                    json_info.append(jso)

                    # 多线程
                    # result = self.mysql_insert(info)

                _page = soup.find('div', class_="result-page")
                if _page:
                    result_page = _page.find('ul').find_all('li')
                    if result_page[-1].get_text() == '下一页':
                        # 计算数据总条数，如果大于80条，则按80条处理，否则为 页数*10，可能会多
                        count = int(result_page[-2].get_text()) * 10
                    else:
                        count = int(result_page[-1].get_text()) * 10
                else:
                    count = len(content_result) if content_result else 0
            else:
                json_info = []
                count = 0

            result = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'total': count,
                    'result': json_info
                }
            }
            return json.dumps(result, indent=1)  # , count  字典转换为json，并格式化
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

    # 遍历页数与总条数
    def get_record_sum(self, query, page):
        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page
        try:
            soup = self.get_info(self.zhihu_url, **self.data)
            result_page = soup.find('div', class_="result-page").find('ul').find_all('li')
            if result_page[len(result_page)].get_text() == '下一页':
                page = len(result_page) - 1
                self.get_record_sum(self.zhihu_url, query, page)
            else:
                page = len(result_page)
                page_num = int(result_page[page].get_text())
                sum = page_num * 10  # 计算不精确，可能会少1-9条
        except Exception, e:
            return

    def get_text(self, url):
        '''
        :param url: 访问的url地址
        :return: 获取text内容
        '''
        detail_info = {}

        soup = self.get_info(url)
        title = soup.find('div', attrs={'id': "zh-question-title", 'data-editable': "false"}).find(
            'h2', class_='zm-item-title').find('span', class_="zm-editable-content").get_text()
        detail_info['title'] = title  # 标题

        text = soup.find('div', attrs={'id': "zh-question-detail", 'class': "zm-item-rich-text"}).find(
            'div', class_="zm-editable-content").get_text()
        detail_info['text'] = text  # 内容

        answer = soup.find('div', attrs={'id': "zh-question-answer-wrap", 'class': "zh-question-answer-wrapper"})
        answer_head = answer.find_all('div', class_="answer-head")  # auther
        answer_text = answer.find_all('div', class_='zm-editable-content clearfix')  # answer text
        if answer_head:
            info_list = []
            for i, j in zip(answer_head, answer_text):
                # print(i.find('a', class_="author-link").get_text() if \
                #     i.find('a', class_="author-link") else i.find('span', class_='name').get_text())
                # print(j.get_text())
                info = {}
                info['author'] = i.find('a', class_="author-link").get_text() if \
                    i.find('a', class_="author-link") else i.find('span', class_='name').get_text()
                info['content'] = j.get_text()
                info_list.append(info)
            detail_info['answer'] = info_list
        else:
            detail_info['answer'] = []
        return detail_info  # json.dumps(detail_info, indent=1)


if __name__ == '__main__':
    query = '品尚汇仁'
    page = 1
    site = ('101', '102')
    zhihu = Sogou_zhihu()
    result = zhihu.get_html_info(query, page)
    print(result)
