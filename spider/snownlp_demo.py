#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/16 13:18
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
from snownlp import SnowNLP
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

s = SnowNLP(u'这个东西真心好用,好屌')
for i in s.words: print(i)
for i in s.tags: print(i)

print(s.sentiments)  # positive的概率 积极、正确
print(s.pinyin)  # 拼音

m = SnowNLP(u'「繁體字」「繁體中文」的叫法在臺灣亦很常見。')
print(m.han)  # 繁体转简体

text = u'''
自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
所以它与语言学的研究有着密切的联系，但又有重要的区别。
自然语言处理并不是一般地研究自然语言，
而在于研制能有效地实现自然语言通信的计算机系统，
特别是其中的软件系统。因而它是计算机科学的一部分。
'''
ss = SnowNLP(text)
for i in ss.keywords(10): print(i) # 词组，默认5个

for i in ss.summary(3): print(i) #概括，总结的
print('\n\n')
for i in ss.sentences: print(i) #句子

sss = SnowNLP([[u'这篇', u'文章'],
             [u'那篇', u'论文'],
             [u'这个'],
               [u'这个'],
               [u'文章',u'句子']])
for i in sss.tf:print(i)
for i in sss.idf:print(i.decode())

print(sss.sim([u'文章'])) # [0.3756070762985226, 0, 0]