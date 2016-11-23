#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/23 16:15
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

from sogou import sogou
import datetime
import json


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
        self.data['word'] = query
        self.data['pn'] = (page - 1) * 20
        try:
            self.soup = self.get_info(self.baidu_news_url, **self.data)

            news = self.soup.find_all('div', class_="result")
            news_list = []
            for new in news:
                n = {}
                # 取出新闻链接地址
                n['url'] = new.a.get('href').encode("utf-8")

                # 取出新闻标题
                news_title = ''
                for t in new.a.contents:
                    if t != '\n':
                        news_title = news_title + t.string
                n['title'] = news_title.encode("utf-8")

                # 取出新闻来源和时间

                news_source = new.find('p', class_='c-author').string

                n['website_name'] = news_source.encode("utf-8")

                # 取出新闻简介
                news_contents = ''
                for c in new.p.contents:
                    if c != '\n':
                        news_contents = news_contents + c.string.encode("utf-8")

                n['txt'] = news_contents

                # 相似新闻数量
                sim = new.span.a.string
                if len(sim) != 0:
                    sim_count = ''
                    for words in list(sim):
                        if words in range(0, 10):
                            sim_count = str(sim_count) + str(words)

                    n['sim_count'] = str(sim_count)
                else:
                    n['sim_count'] = 0

                news_list.append(n)
            counts = self.soup.find('div', attrs={'id':'header_top_bar'}).find('span',class_='nums').get_text()
            count = counts[7:-1]

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

    '''
    def url(self):

        return "http://news.baidu.com/ns?from=news&q1=%s&rn=%d" % (self.keywords, self.number)

    def get_news(self):

        pages = urllib2.urlopen(self.url())
        Html = BeautifulSoup(pages.read(),"html.parser")
        news = Html.find_all('div', class_="result")

        news_list = {}
        k = 1
        for new in news:
            n = {}
            # 取出新闻链接地址
            n['url'] = new.a.get('href').encode("utf-8")

            # 取出新闻标题
            news_title = ''
            for t in new.a.contents:
                if t != '\n':
                    news_title = news_title + t.string
            n['title'] = news_title.encode("utf-8")

            # 取出新闻来源和时间

            news_source = new.find('p', class_='c-author').string

            n['website_name'] = news_source.encode("utf-8")

            # 取出新闻简介
            news_contents = ''
            for c in new.p.contents:
                if c != '\n':
                    news_contents = news_contents + c.string.encode("utf-8")

            n['txt'] = news_contents

            # 相似新闻数量
            sim = new.span.a.string
            if len(sim) != 0:
                sim_count = ''
                for words in list(sim):
                    if words in range(0, 10):
                        sim_count = str(sim_count) + str(words)

                n['sim_count'] = str(sim_count)
            else:
                n['sim_count'] = 0

            news_list[k] = n

            k += 1

        return news_list
'''

if __name__ == '__main__':
    query = '广发银行'
    page = 1
    baidu = Baidu_news()
    result = baidu.get_html_info(query,page)
    print(result)
