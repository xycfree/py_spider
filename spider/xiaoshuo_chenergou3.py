#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/2 10:42
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
from bs4 import BeautifulSoup
import lxml
import re
import requests
from threading import Thread
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

down_path = 'txt/'
url = 'http://www.xiaoshuo2016.com/'  # 主页
files = 'files/article/html/3/3209/'  # 小说陈二狗3
# url1 =  'http://www.xiaoshuo2016.com/files/article/html/3/3209/36347442.html'
page_num = 36347442  # 第一章节页数
extension = '.html'  # 扩展名


def get_txt(url, files, page_num, extension):
	t = page_num
	for i in range(5):
		urls = url + files + str(t) + extension
		r = requests.get(urls, stream=True)  #
		soup = BeautifulSoup(r.content, 'lxml')
		# print 'soup: ', soup

		txt = str(soup.find('p'))
		m = re.sub('<br/>|</p>|<p>|http://','',txt) #文本替换，替换类型，替换内容，文本内容
		#print 'm: ',m
		filename = down_path + str(t) + '.txt'
		with open(filename, 'wb') as f:
			f.writelines(m)
		t += 1


if __name__ == '__main__':
	get_txt(url, files, page_num, extension)
