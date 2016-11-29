#!/usr/bin/env python
# coding:utf-8
__author__ = 'Administrator'

import unittest
import threading
from mysql_conn import Mysql


class MyTestCase(threading.Thread):

    def test_get_all(self):
        try:
            mysql = Mysql()
            query = 'SELECT * FROM craw_data'
            result = mysql.get_all(query)
            if result:
                print 'get all'
                for row in result:
                    print row
            else:
                print('select is none')
        except  Exception, e:
            print str(e)



    def test_thread(self):
        threads = []
        for i in range(5):
            t = threading.Thread(target=MyTestCase.test_get_all)  #
            # t.setName('threads ...') #设置
            # print t.getName() #获取线程名称
            # t.setDaemon(True) #threading.setDaemon()的使用。设置后台进程
            threads.append(t)
            t.start()


def test_insert_one():
    try:
        mysql = Mysql()
        query = "INSERT INTO craw_data (keywords,title,url,intro,details) VALUES (%s,%s,%s,%s,%s)"
        result = mysql.insert_one(query, ('111', '2222', '333', '444', '4555'))
        print(result)
    except Exception, e:
        raise

if __name__ == '__main__':
   # unittest.main()
    test_insert_one()