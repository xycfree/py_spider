#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-06 21:53:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $

import os

DBHOST = "127.0.0.1" # 数据库
DBPORT = 3306 # 端口
DBUSER = "root" # 用户名
DBPWD = "root" # 密码
DBNAME = "jfpython" # 数据库
DBCHAR = "utf8" # 编码方式

'''
当然，还有很多其他参数可以配置：

dbapi ：数据库接口
mincached ：启动时开启的空连接数量
maxcached ：连接池最大可用连接数量
maxshared ：连接池最大可共享连接数量
maxconnections ：最大允许连接数量
blocking ：达到最大数量时是否阻塞
maxusage ：单个连接最大复用次数
'''