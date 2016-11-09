#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-06 21:53:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $

import os
import re
from bs4 import BeautifulSoup
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Lagou_info(object):
	def __init__(self):
		self.url_base = r'https://www.lagou.com/jobs/list_'  # 查询公司url前缀
		self.static_url = r'https://www.lgstatic.com/'  # 静态图片url前缀
		self.url_position = r'https://www.lagou.com/gongsi/searchPosition.json'  # 所有职位url，json格式
		self.position_base = r'https://www.lagou.com/jobs/'  # 2556926.html' 职位url前缀
		self.question = r'https://www.lagou.com/gongsi/q'  # 35422.html 公司问答 url前缀
		self.html = r'.html'  # Url地址后缀
		self.http = r'https:'

	def get_company_url(self, comp_name):
		'''根据公司名称获取url地址
		:param comp_name: 需要查询的公司名
		:return: 返回拉钩网该公司的主页URL
		'''
		# url_base = 'https://www.lagou.com/jobs/list_'
		urls = self.url_base + comp_name
		data = {
			'labelWords': '',
			'fromSearch': 'true',
			'suginput': ''
		}
		try:
			r = requests.get(urls, params=data, timeout=6).content
			soup = BeautifulSoup(r, 'lxml')
			url = soup.find('div', attrs={'class': 'cl_r_top'}).find('a').get(
				'href')  # //www.lagou.com/gongsi/35422.html
			return url
		except Exception, e:
			return str(e)

	def get_company_info(self, url):
		'''请求url,得到返回信息，并通过lxml解析
		:param url: 企业在拉钩上的主页
		:return: 返回公司HTML, 公司ID, 招聘职位数
		'''
		company_id = url[23:-5]  # 公司Id  url:https://www.lagou.com/gongsi/138877.html
		# print('company_id: {}'.format(company_id))
		req_url = self.http + url
		try:
			r = requests.get(req_url, timeout=6).content
			soup = BeautifulSoup(r, 'lxml')

			top_info = soup.find('div', class_='top_info_wrap')
			comp_data = top_info.find('div', class_='company_data').select('strong')[0].get_text().strip()  # 招聘职位数
			return soup, company_id, comp_data
		except Exception, e:
			return str(e)

	def get_comp_recruit_info(self, soup):
		'''公司招聘信息：公司logo, 公司url, 公司名称, 招聘职位数, 简历及时处理率, 简历处理用时, 面试评价, 企业最近登录
		:param soup: 公司HTML信息
		:return 公司招聘信息
		'''
		recruit_info = {}
		top_info = soup.find('div', class_='top_info_wrap')
		comp_logo = self.http + top_info.find('img').get('src')  # 公司logo
		comp_url = top_info.find('div', class_='company_info').find('div', class_='company_main').find('a').get(
			'href')  # 公司URL
		comp_name = top_info.find('div', class_='company_info').find('div', class_='company_main').find('a').get(
			'title')  # 公司名称
		company_datas = top_info.find('div', class_='company_data').select('strong')
		company_data = company_datas[0].get_text().strip()  # 招聘职位数
		treatment_rate = company_datas[1].get_text().strip()  # 简历及时处理率
		treatment_time = company_datas[2].get_text().strip()  # 简历处理用时
		audition_eval = company_datas[3].get_text().strip()  # 面试评价
		comp_late_login = company_datas[4].get_text().strip()  # 企业最近登录

		recruit_info['comp_logo'] = comp_logo
		recruit_info['comp_url'] = comp_url
		recruit_info['comp_name'] = comp_name
		recruit_info['company_data'] = company_data
		recruit_info['treatment_rate'] = treatment_rate
		recruit_info['treatment_time'] = treatment_time
		recruit_info['audition_eval'] = audition_eval
		recruit_info['comp_late_login'] = comp_late_login
		return recruit_info

	def get_comp_basic_info(self, soup):
		'''公司基本信息: 所属行业, 公司性质, 公司规模, 公司地址
		:param soup:
		:return:
		'''
		basic_info = {}
		basic_container = soup.find('div', attrs={'class': 'item_container', 'id': 'basic_container'})
		industryField = basic_container.find('ul').select('span')[0].get_text()  # 所属行业
		financeStages = basic_container.select('span')
		financeStage = financeStages[1].get_text()  # 公司性质
		companySize = financeStages[2].get_text()  # 公司规模
		# address = financeStages[3].get_text() #公司地址
		basic_info['industryField'] = industryField
		basic_info['financeStage'] = financeStage
		basic_info['companySize'] = companySize
		# basic_info['address'] = address
		return basic_info

	def get_comp_product_info(self, soup):
		'''公司产品
		:param soup:
		:return:
		'''
		product_info = {}
		company_products = soup.find('div', attrs={'class': 'item_container', 'id': 'company_products'})
		if company_products:
			products = company_products.find_all('div', class_='product_url')
			product = [i.find('a').get_text().strip() for i in products]  # 公司产品
		else:
			product = None
		product_info['product'] = product
		return product_info

	def get_comp_introduce_info(self, soup):
		'''公司介绍： 公司介绍,公司图片
		:param soup:
		:return:
		'''
		introduce_info = {}
		company_intro = soup.find('div', attrs={'class': 'item_container', 'id': 'company_intro'})
		comp_content = company_intro.find('span', class_='company_content').get_text()  # 公司介绍
		comp_imgs = company_intro.find('ul', attrs={'class': 'company_img', 'id': 'rotateImages'}).find_all('li') if \
			company_intro.find('ul', attrs={'class': 'company_img', 'id': 'rotateImages'}) else None
		comp_img = [self.static_url + i.get('data-item') for i in comp_imgs] if comp_imgs else None  # 公司图片

		introduce_info['comp_content'] = comp_content
		introduce_info['comp_img'] = comp_img
		return introduce_info

	def get_comp_interview_info(self, soup):
		'''面试评价
		:param soup:
		:return:
		'''
		interview_info = {}
		interview_container = soup.find('div', attrs={'id': 'interview_container'})
		if interview_container.find('div', class_='comprehensive-review clearfix'):
			comprehensive_score = interview_container.find('div', class_='comprehensive-review clearfix') \
				.find('span', class_='score').get_text()  # 综合评分
			total_score = interview_container.find('ul', class_='classification-review clearfix').find_all(
				'span', class_='score')
			detail_score = total_score[0].get_text()  # 描述相符评分
			interviewer_score = total_score[1].get_text()  # 面试官评分
			comp_environment_score = total_score[2].get_text()  # 公司环境评分
		else:
			comprehensive_score, detail_score, interviewer_score, comp_environment_score = None, None, None, None

		interview_info['comprehensive_score'] = comprehensive_score
		interview_info['detail_score'] = detail_score
		interview_info['interviewer_score'] = interviewer_score
		interview_info['comp_environment_score'] = comp_environment_score

		return interview_info

	def get_comp_address_info(self, soup):
		'''公司办公地址 市、区,办公地址
		:param soup:
		:return:
		'''
		address_info = {}
		address_container = soup.find('div',
		                              attrs={'class': 'address_container item_container', 'id': 'location_container'})
		mlist_total = address_container.find('span', class_='mlist_total').get_text()  # 公司地址数量
		if int(mlist_total) > 0:
			city_district = [i.get_text().strip() for i in
			                 address_container.find_all('span', class_='li_title_text ellipsis')]  # 市，区
			address = [i.get_text().strip() for i in address_container.find_all('p', class_='mlist_li_desc')]  # 办公地址
			city_dist_addr = zip(city_district, address)
		else:
			# city_district = None
			# address = None
			city_dist_addr = None

		address_info['city_dist_addr'] = city_dist_addr
		return address_info

	def get_comp_manager_info(self, soup):
		'''管理团队
		:param soup:
		:return:
		'''
		manager_info = {}
		comp_manger = soup.find('div', class_='company_managers item_container')
		if comp_manger:
			manager_name = comp_manger.find('p', class_='item_manager_name').find('span').get_text() if \
				comp_manger.find('p', class_='item_manager_name') else None  # 管理人名称
			manager_title = comp_manger.find('p', class_='item_manager_title').get_text() if \
				comp_manger.find('p', class_='item_manager_title') else None  # 管理人title
			manager_content = comp_manger.find('div', class_='item_manager_content').get_text() if \
				comp_manger.find('div', class_='item_manager_content') else None  # 管理人简介
			manager_info['manager_name'] = manager_name
			manager_info['manager_title'] = manager_title
			manager_info['manager_content'] = manager_content
		else:
			manager_info['manager_name'], manager_info['manager_title'], manager_info[
				'manager_content'] = None, None, None
		return manager_info

	def get_comp_tags_info(self, soup):
		'''公司标签
		:param soup:
		:return:
		'''
		tags_info = {}
		tags_container = soup.find('div', class_='tags_container item_container')
		if tags_container:
			comp_labels = tags_container.find('ul', class_='item_con_ul clearfix').select('li')
			comp_label = [i.get_text().strip() for i in comp_labels]  # 公司标签
		else:
			comp_label = None
		tags_info['comp_label'] = comp_label
		return tags_info

	def get_comp_position_info(self, company_id, comp_data):
		'''查询公司所有招聘的职位
		:param company_id: 公司id
		:param company_data: 公司招聘职位数
		:return: 列表形式返回所有职位信息
		'''
		info_list = []
		if comp_data.isdigit():
			total_page = comp_data / 10 + 1 if comp_data % 10 else comp_data / 10  # 招聘职位数分页
			page = 1
			data = {
				'companyId': company_id,
				'positionFirstType': '全部',
				# 'pageNo' : page,
				'pageSize': 10
			}

			for i in range(total_page):
				data['pageNo'] = page
				json = requests.get(self.url_position, params=data, timeout=6).json()
				list_con = json['content']['data']['page']['result']  # 所有职位信息
				for j in list_con:
					info = []
					job = j['positionId']  # 职位ID
					job_url = self.position_base + str(job) + self.html  # 职位url
					info.append(job_url)
					info.append(j['positionName'])  # 职位
					info.append(j['city'])  # 地点
					info.append(j['salary'])  # 薪资
					info.append(j['workYear'])  # 工作经验
					info.append(j['education'])  # 学历
					info.append(j['jobNature'])  # 工作性质
					info.append(j['createTime'])  # 发布时间 今天发布显示为时间，其他显示为日期 datetime.datetime.now().strftime('%Y-%m-%d')

					info_list.append(info)
				page += 1
		return info_list

	def get_comp_question_info(self, company_id):
		url = self.question + str(company_id) + self.html
		question_info = {}
		try:
			r = requests.get(url, timeout=6).content
			soup = BeautifulSoup(r, 'lxml')
			question_container = soup.find('div', class_='company-info')
			if question_container:
				question_nums = question_container.find('ul', attrs={'class':'items-infos'}).find_all('li')
				question_num = question_nums[0].find('span').get_text()  # 问题数量
				answers_num = question_nums[1].find('span').get_text()  # 回答数量
				follow_num = question_nums[2].find('span').get_text() # 关注数量
			else:
				question_num,answers_num,follow_num=None,None,None
			question_info['question_num'] = question_num
			question_info['answers_num'] = answers_num
			question_info['follow_num'] = follow_num

			question_answer_list = soup.find('ul',attrs={'id':'question-answer-list'}).find_all('li',class_='items-question clearfix')
			question_list = []
			for i in question_answer_list:
				info = []
				info.append(self.http + i.find('a',class_='item-question').get('href')) #问答网址
				#print(self.http + i.find('a',class_='item-question').get('href'))
				info.append(i.find('a',class_='item-question').get_text()) #问题
				#print(i.find('a',class_='item-question').get_text())
				info.append(i.find('textarea', class_="answer-html").get_text()) #回答
				#print(i.find('textarea', class_="answer-html").get_text())
				question_list.append(info)
			question_info['question_list'] = question_list
			return question_info
		except Exception, e:
			return str(e)


if __name__ == '__main__':
	# url = get_company_url('至恒信息')
	# get_company_info(url)
	# position_all('35422',133)
	comp_name = '京东'
	lagou = Lagou_info()
	u = lagou.get_company_url(comp_name)
	soup, company_id, comp_data = lagou.get_company_info(u)
	# print('{0},招聘信息: {1}'.format(comp_name, lagou.get_comp_recruit_info(soup)))
	# print('{0},办公地址: {1}'.format(comp_name, lagou.get_comp_address_info(soup)))
	# print('{0},公司基本信息: {1}'.format(comp_name, lagou.get_comp_basic_info(soup)))
	# print('{0},面试评价: {1}'.format(comp_name, lagou.get_comp_interview_info(soup)))
	# print('{0},管理团队: {1}'.format(comp_name, lagou.get_comp_manager_info(soup)))
	# print('{0},公司介绍: {1}'.format(comp_name, lagou.get_comp_introduce_info(soup)))
	# print('{0},公司产品: {1}'.format(comp_name, lagou.get_comp_product_info(soup)))
	# print('{0},公司标签: {1}'.format(comp_name, lagou.get_comp_tags_info(soup)))
	# print('{0},招聘职位详细信息: {1}'.format(comp_name, lagou.get_comp_position_info(company_id,comp_data)))
	print('{0},招聘职位详细信息: {1}'.format(comp_name,lagou.get_comp_question_info(company_id)))
