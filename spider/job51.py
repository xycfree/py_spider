#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/9 22:35
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import requests
from bs4 import BeautifulSoup
import datetime
import time

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Job51_info(object):
	def __init__(self):
		self.url_base = r'http://search.51job.com/list/000000,000000,0000,00,9,99,'  # 51job url前缀
		self.url_html = r',1,1.html'  # url后缀
		self.posi_url = r'http://search.51job.com/jobsearch/search_result.php'  # 职位页url

	def get_company_info(self, company_name):
		'''
		:param company_name: 查询的公司名称
		:return:
		'''
		url = self.url_base + company_name + self.url_html
		data = {
			'lang': 'c',
			'stype': 1,
			'postchannel': 0000,
			'workyear': 99,
			'cotype': 99,
			'degreefrom': 99,
			'jobterm': 99,
			'companysize': 99,
			'lonlat': '0,0',
			'radius': -1,
			'ord_field': 0,
			'confirmdate': 9,
			'fromType': '',
			'dibiaoid': 0,
			'address': '',
			'line': '',
			'specialarea': 00,
			'from': '',
			'welfare': '',
		}
		try:
			r = requests.get(url, params=data, timeout=6).content
			soup = BeautifulSoup(r, 'lxml')
			return soup
		except Exception, e:
			return str(e)

	def get_comp_position_info(self, soup, company_name):
		'''
		:param soup: html信息
		:param company_name: 公司名称
		:return:
		'''
		position_info = {}
		posi_list = []
		position_all = soup.find('div', attrs={'class': "dw_table", 'id': "resultList"}).find_all(
			'div', attrs={'class': 'el'})[1:]  # 获取所有职位信息 [0]为<div class="el title"> 标题
		position_num = soup.find('div', attrs={'class': "dw_table", 'id': "resultList"}
		                         ).find_all('div', class_='rt')[0].get_text().strip()[1:-3]  # 职位总数
		if int(position_num) > 0:
			pages = soup.find('div', attrs={'class': "dw_table", 'id': "resultList"}).find_all(
				'div', class_='rt')[1].get_text().strip().split('/')  # 页数
			posi_page, posi_sum_page = pages  # 当前页，总页数
			posi_page = int(posi_page.strip())
			posi_sum_page = int(posi_sum_page.strip())

			if posi_sum_page == 1: #判断有几页数据
				for i in position_all:
					if i.find('span', class_='t2').find('a').get_text() == company_name:
						info = []
						info.append(i.find('p', class_='t1').find('a').get_text().strip())  # 职位名称
						info.append(i.find('p', class_='t1').find('a').get('href').strip())  # 职位url
						info.append(i.find('span', class_='t2').find('a').get_text().strip())  # 公司名称
						info.append(i.find('span', class_='t3').get_text().strip())  # 工作地点
						info.append(i.find('span', class_='t4').get_text().strip())  # 薪资范围
						info.append(i.find('span', class_='t5').get_text().strip())  # 发布时间
						posi_list.append(info)
			else:
				posi_list= self.get_position_all_info(company_name,posi_page,posi_sum_page)

		position_info['posi_list'] = posi_list
		return position_info

	def get_position_all_info(self, company_name, posi_page, posi_sum_page):
		
		data = {
			'fromJs': 1,
			'jobarea': '000000,00',
			'district': 000000,
			'funtype': 0000,
			'industrytype': 00,
			'issuedate': 9,
			'providesalary': 99,
			'keyword': company_name,
			'keywordtype': 1,
			#'curr_page': 2,
			'lang': 'c',
			'stype': 1,
			'postchannel': 0000,
			'workyear': 99,
			'cotype': 99,
			'degreefrom': 99,
			'jobterm': 99,
			'companysize': 99,
			'lonlat': '0,0',
			'radius': -1,
			'ord_field': 0,
			'list_type': 0,
			'fromType': 14,
			'dibiaoid': 0,
			'confirmdate': 9
		}
		posi_list = []
		while posi_page <= posi_sum_page:
			data['curr_page'] = posi_page
			print('posi_page: {0}'.format(posi_page))
			print(datetime.datetime.now())
			r = requests.get(self.posi_url, params=data,timeout=6).content
			soup = BeautifulSoup(r,'lxml')

			position_all = soup.find('div', attrs={'class': "dw_table", 'id': "resultList"}).find_all(
				'div', attrs={'class': 'el'})[1:]  # 获取所有职位信息 [0]为<div class="el title"> 标题
			for i in position_all:
				if i.find('span', class_='t2').find('a').get_text() == company_name:
					info = []
					info.append(i.find('p', class_='t1').find('a').get_text().strip())  # 职位名称
					info.append(i.find('p', class_='t1').find('a').get('href').strip())  # 职位url
					info.append(i.find('span', class_='t2').find('a').get_text().strip())  # 公司名称
					info.append(i.find('span', class_='t3').get_text().strip())  # 工作地点
					info.append(i.find('span', class_='t4').get_text().strip())  # 薪资范围
					info.append(i.find('span', class_='t5').get_text().strip())  # 发布时间
					posi_list.append(info)
			posi_page += 1
		print(datetime.datetime.now())
		print(time.time())
		return posi_list

if __name__ == '__main__':
	company_name = '小米通讯技术有限公司'
	job51 = Job51_info()
	comp_info = job51.get_company_info(company_name)
	#print(comp_info)
	comp_posi_info = job51.get_comp_position_info(comp_info, company_name)
	print(comp_posi_info)
	print(datetime.datetime.now())
	print(time.time())


