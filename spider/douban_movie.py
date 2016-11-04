#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/2 21:10
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import requests
import re
import codecs
from bs4 import BeautifulSoup
from openpyxl import Workbook
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

wb = Workbook()
path = 'download/'
dest_filename = path + u"电影.xlsx"
ws1 = wb.active
ws1.title = u'电影top250'
DOWNLOAD_URL = 'https://movie.douban.com/top250'

if not os.path.exists(path):
	os.mkdir(path)

def download_page(url):
	'''
	:param url: 网页地址
	:return: 返回页面内容
	'''
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
		 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
	}
	data = requests.get(url, headers=headers).content
	return data


def get_movie(doc):
	'''
	:param doc: 豆瓣电影，top250的电影信息
	:return:
	'''
	soup = BeautifulSoup(doc, 'lxml')
	ol = soup.find('ol', class_='grid_view')
	mov_url = []  # 电影url
	name = []  # 电影名字
	star_con = []  # 评价人数
	score = []  # 评分
	info_list = []  # 短评
	for i in ol.find_all('li'):
		detail = i.find('div', class_='info')  # 'div', attrs={'class': 'hd'} 或 'div',class_='hd'
		# print detail
		movie_url = detail.find('a', attrs={'class': ''}).get('href')  # 获取电影页面连接
		# print('movie_url: ',movie_url),type(movie_url)
		movie_name = detail.find('span', attrs={'class': 'title'}).get_text()
		# print movie_name
		level_star = detail.find('span', attrs={'class': 'rating_num'}).get_text()
		# print level_star
		star = detail.find('div', attrs={'class': 'star'}).find_all('span')  # 获取所有span
		star_num = star[3].getText()[:-3]  # 146914 人评价去掉
		# print star_num
		info = detail.find('span', attrs={'class': 'inq'})
		# print info
		if info:
			info_list.append(info.get_text())  # 短评
		else:
			info_list.append('无')
		score.append(level_star)  # 评分
		name.append(movie_name)  # 电影名
		mov_url.append(movie_url)  # 电影地址
		star_con.append(star_num)  # 评价人数

	page = soup.find('span', attrs={'class': 'next'}).find('a')  # 获取下一页
	if page:
		return mov_url, name, star_con, score, info_list, DOWNLOAD_URL + page['href']
	return mov_url, name, star_con, score, info_list, None


def main():
	url = DOWNLOAD_URL
	mov_url = []
	name = []
	star_con = []
	score = []
	info = []
	while url:
		doc = download_page(url)
		m_url, m_name, star, level_num, info_list, url = get_movie(doc)
		# mov_url.append(m_url)
		# name.append(m_name)
		# star_con.append(star)
		# score.append(level_num)
		# info.append(info_list)
		mov_url = mov_url + m_url
		name = name + m_name
		star_con = star_con + star
		score = score + level_num
		info = info + info_list

	try:
		ws1['A1'] = 'Url'
		ws1['B1'] = 'name'
		ws1['C1'] = 'star'
		ws1['D1'] = 'score'
		ws1["E1"] = 'info'
		for (a1, b1, c1, d1, e1) in zip(mov_url, name, star_con, score, info):
			col_A = 'A%s' % (mov_url.index(a1) + 2)  # str.index(str, beg=0, end=len(string)) 检索
			col_B = 'B%s' % (mov_url.index(a1) + 2)
			col_C = 'C%s' % (mov_url.index(a1) + 2)
			col_D = 'D%s' % (mov_url.index(a1) + 2)
			col_E = 'E%s' % (mov_url.index(a1) + 2)

			ws1[col_A] = a1
			ws1[col_B] = b1
			ws1[col_C] = c1
			ws1[col_D] = d1
			ws1[col_E] = e1
	except Exception, e:
		print 'Except: ', str(e)
	wb.save(filename=dest_filename)


if __name__ == '__main__':
	main()
