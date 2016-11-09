#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/3 10:53
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

down_path = 'download/'
down_file = u'拉钩招聘.xlsx'

if not os.path.exists(down_path):
	os.mkdir(down_path)


def get_json(url, page, lang_name):
	'''
	:param 拉钩招聘信息
	:param url: Request URL:https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false
	:param data:  URL请求的From data
	:param page: 请求页数
	:param lang_name: 搜索的关键字
	:return:
	'''
	data = {'first': 'true', 'pn': page, 'kd': lang_name}
	json = requests.post(url, data).json()
	list_con = json['content']['positionResult']['result']
	info_list = []

	for i in list_con:
		info = []
		info.append(i['companyShortName'])  # 公司简称
		info.append(i['companyFullName'])  # 公司全名
		info.append(i['city'])  # 城市
		info.append(i['positionName'])  # 招聘职位
		info.append(i['workYear'])  # 工作年限
		info.append(i['education'])  # 学历
		info.append(i['salary'])  # 薪资
		info.append(i['jobNature'])  # 工作性质
		info.append(i['industryField'])  # 行业类别
		info.append(i['financeStage'])  # 公司财务类型

		# lab_li = li_to_tu(i['companyLabelList']) #公司标签遍历方法
		info.append(','.join(tuple(i['companyLabelList'])[:]) if i[
			'companyLabelList']  else '')  # 公司标签 if i['companyLabelList']: ','.join(tuple(i['companyLabelList'])[:]) else ''
		info.append(i['companySize'])  # 公司规模
		info_list.append(info)
	return info_list


# 遍历公司标签
def li_to_tu(li):
	if li:
		ll = ','.join(tuple(li)[:])
	else:
		ll = ''
	return ll


def main(lang_name):
	#lang_name = raw_input('职位名: ')
	page = 1
	url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'  # 城市 city=成都&needAddtionalResult=false
	info_result = []
	while page < 10:
		info = get_json(url, page, lang_name)
		info_result = info_result + info
		page += 1

	wb = Workbook()
	ws1 = wb.active
	ws1.title = unicode(lang_name)
	# ws1['A1'] = '公司简称' #增加列标题
	ws1.append([u'公司简称', u'公司全称', u'城市', u'招聘职位', u'工作年限', u'学历', u'薪资',
	            u'工作性质', u'行业类别', u'公司财务类型', u'公司标签', u'公司规模'])
	for row in info_result:
		ws1.append(row)

	wb.save(down_path + down_file) #excel保存


if __name__ == '__main__':
	main()
