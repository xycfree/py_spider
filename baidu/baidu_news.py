#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/23 16:15
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

from sogou import sogou
import datetime
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Baidu_news(sogou.Sogou):
    def __init__(self):
        super(Baidu_news, self).__init__()
        self.data = {
            # 'word': (unable to decode value),
            # 'pn': 0,
            'tn': 'news', # news newstitle 新闻全文，新闻标题
            # 'from': 'news',
            'cl': 2,
            'rn': 20,
            'ct': 1,
            'ie': 'utf-8',
            'bt': 0,
            'et': 0,
            'clk': 'ortbytime' # ortbytime sortbyrel 按时间排序，焦点排序
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
        self.data['word'] = '"' + query + '"'
        self.data['pn'] = (page - 1) * 20
        try:
            self.soup = self.get_info(self.baidu_news_url, **self.data)
            news_list = []
            news = self.soup.find_all('div', class_="result")
            for new in news:
                n = {}
                n['keywords'] = query # 关键词
                n['url'] = new.a.get('href') #.encode("utf-8") # 取出新闻链接地址
                n['title'] = new.a.get_text() #标题
                #print(n['title'])
                m = new.find('p', class_='c-author').get_text().encode('utf-8').strip() # 取出新闻来源和时间
                #m = m.replace('  ', ',')
                source = re.split('  ', m)
                n['website'] = source[0] # 来源站点
                n['time'] = source[1] # 时间
                # print('{0},{1}'.format(n['website'],n['time']))
                #n['intro'] = new.find('div', class_="c-summary c-row ").get_text() #简介



                # 取出新闻简介
                p_text = new.find('p', class_='c-author')
                news_contents = ''
                text = p_text.next_sibling
                while True:
                    if text.name == None or text.name == 'em':
                        news_contents = unicode(news_contents) + unicode(text)
                        text = text.next_sibling
                    elif text.name == 'span':
                        break
                n['intro'] = news_contents

                # 相似新闻数量
                n['sim_count'] = new.find('a', class_="c-more_link").get_text()[:-5] if new.find(
                    'a', class_="c-more_link") else 0
                news_list.append(n)

            counts = self.soup.find('div', attrs={'id': 'header_top_bar'}).find('span', class_='nums').get_text()
            count = counts[6:-1] if len(counts) == 8 else counts[7:-1]
            # print(len(counts))
            result = {
                'code': 0,
                'msg': '成功',
                'data': {
                    'total': count,
                    'result': news_list
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
    query = '广发银行'
    page = 1
    baidu = Baidu_news()
    result = baidu.get_html_info(query,page)
    print(result)
