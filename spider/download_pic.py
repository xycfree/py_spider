#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-17 10:08:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
import urllib
from bs4 import BeautifulSoup
import lxml
import threading



pic_path = 'pic'  # 保存文件路径

URL = 'http://www.nanrenwo.net/z/tupian/hashiqitupian/'
URL1 = 'http://www.nanrenwo.net'

class Download_pic():


    def download_pic(self,url, src, filename):
        '''
        图片文件下载到本地 request url, img src,img name
        '''
        # filename = os.path.split(url)[1] #判断URL的文件
        # if not filename:
        #     filename = 'default.jpg'
        filename = os.path.join(pic_path,filename) #文件路径+文件名称
        u = url + src
        r = requests.get(u, stream=True)
        chunk_size = 4096  # 写入图片大小
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
        return True

    # download_pic(URL)


    def down_pic(self,url):
        t = 1
        r = requests.get(url, stream=True)
        soup = BeautifulSoup(r.text, 'lxml')
        # print soup.prettify() #html机构
        # print soup.title
        # print soup.head
        # print soup.body
        #print soup.select('.waterfall')
        #print soup.find_all(id='brand-waterfall')
        #print soup.find_all('a')


        # for myimg in soup.find_all('a'):  # soup.find_all('a') 查询HTML内所有连接 <a>
        #     if myimg.find('img') and ('.jpg' in myimg.find('img').get('src')):  # <a> 内含有 img 元素
        #         pic_name = str(t) + '.jpg'
        #         img_src = myimg.find('img').get('src')  # 得到src信息
        #         print img_src
        #         download_pic(URL1,img_src,pic_name)
        #         t += 1

        myimg = [img.get('src') for img in soup.find(id='brand-waterfall').find_all('img')]  #查询id下所有img元素
        print 'myimg:',myimg
        print '*********'*5
        for img in myimg:
            pic_name = str(t) + '.jpg'
            #img_src = img.get('src')
            print 'img: ',img
            self.download_pic(URL1,img,pic_name) #request Url,img src,picture name
            t += 1



d = Download_pic()
d.down_pic(URL)

'''
def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def get_Img(html):
    imglist = re.findall(photo, html)  # 查询
    return imglist
#html =get_html(URL)
#u = get_Img(html)
'''
