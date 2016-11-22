#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/22 9:55
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
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

    def get_html_info(self, query, page=1, time=0, site=100):
        '''
        :param query: 搜索的关键词,默认第一页
        :return: 返回第一页数据
        '''

        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page

        try:
            soup = self.get_info(self.zhihu_url, **self.data)
            box_result = soup.find('div', class_='zhihu-warp').find('div', class_='result-content').find('div', class_="box-result")
            json_info = []
            if box_result:
                content_result = soup.find('div', class_='box-result').find_all('div', class_='result-about-list')
                for i in content_result:
                    jso = {}
                    jso['keywords'] = query
                    jso['title'] = i.find('h4', class_='about-list-title').find('a').get_text()
                    jso['url'] = i.find('h4', class_="about-list-title").find('a').get('href')

                    # text = self.get_text(i.find('h4', class_="about-list-title").find('a').get('href'))
                    # jso['details'] = text # 内容详情
                    json_info.append(jso)

                    # 多线程
                    # result = self.mysql_insert(info)

                result_page = soup.find('div', class_="result-page").find('ul').find_all('li')
                if result_page:
                    if result_page[-1].get_text() == '下一页':
                        # 计算数据总条数，如果大于80条，则按80条处理，否则为 页数*10，可能会多
                        sum = int(result_page[-2].get_text()) * 10
                    else:
                        sum = int(result_page[-1].get_text()) * 10
                else:
                    sum = len(content_result)

            else:
                json_info = []
                sum = 0         # 如果没有值，要返回什么？？？
            json_info.append(sum)
            return sum, json.dumps(json_info, indent=1)  # , count  字典转换为json，并格式化
        except Exception, e:
            print(str(e))
            return

    #遍历页数与总条数
    def get_record_sum(self, query, page):
        self.data['query'] = '"' + query + '"'  # 搜索的关键词，""不拆分关键词搜索
        self.data['page'] = page
        try:
            soup = self.get_info(self.zhihu_url, **self.data)
            result_page = soup.find('div', class_="result-page").find('ul').find_all('li')
            if result_page[len(result_page)].get_text() == '下一页':
                page = len(result_page) - 1
                self.get_record_sum(self.zhihu_url,query, page)
            else:
                page = len(result_page)
                page_num = int(result_page[page].get_text())
                sum = page_num * 10 # 计算不精确，可能会少1-9条
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
        detail_info['title'] = title # 标题

        text = soup.find('div', attrs={'id': "zh-question-detail", 'class': "zm-item-rich-text"}).find(
            'div', class_="zm-editable-content").get_text()
        detail_info['text'] = text # 内容

        answer = soup.find('div', attrs={'id':"zh-question-answer-wrap", 'class':"zh-question-answer-wrapper"})
        answer_head = answer.find_all('div', class_="answer-head") # auther
        answer_text = answer.find_all('div', class_='zm-editable-content clearfix') # answer text
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
    query = '广发银行'
    page = 12
    zhihu = Sogou_zhihu()
    sum,result = zhihu.get_html_info(query, page)
    print(sum)
    print(result)
