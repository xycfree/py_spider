#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-06 21:53:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $

import os
import MySQLdb
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# python MySQL连接池
class Mysql(object):
    '''
    mysql数据库对象，负责产生数据库连接，此类中采用连接池实现获取连接对象，
    conn = Mysql.get_conn()
    conn.close()或del conn
    '''
    # 连接池对象
    __pool = None

    def __init__(self):
        '''
        数据库构造函数，从连接池中取出连接，并生成操作游标
        '''
        self._conn = Mysql.__get_conn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __get_conn():
        '''
        静态方法，从连接池中取出连接
        :return MySQLdb.connection
        '''
        if Mysql.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=200, maxshared=200,
                              maxconnections=300, host=config.DBHOST, port=config.DBPORT,
                              user=config.DBUSER, passwd=config.DBPWD, db=config.DBNAME,
                              use_unicode=False, charset=config.DBCHAR, cursorclass=DictCursor
                              )
            return __pool.connection()

    def get_all(self, sql, param=None):
        '''
        :summary: 执行查询，并取出所有结果集
        :param sql: 查询sql，如有查询条件，请指定条件列表，并将条件值使用param传递
        :param param: 可选参数，条件列表值(元组/列表)
        :return: list(字典对象)/boolean查询到的结果集
        '''
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def get_one(self, sql, param=None):
        '''
        :summary: 执行查询，并取出第一条
        :param sql: 查询sql，如有查询条件，请指定条件列表，并将条件值使用param传递
        :param param: 可选参数，条件列表值(元组/列表)
        :return: list(字典对象)/boolean查询到的结果集
        '''
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def get_many(self, sql, num, param=None):
        '''
        :summary: 执行查询，并取出num条结果
        :param sql: 查询sql，如有查询条件，请指定条件列表，并将条件值使用param传递
        :param sum: 取得的结果条数
        :param param: 可选参数，条件列表值(元组/列表)
        :return: list(字典对象)/boolean查询到的结果集
        '''
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insert_one(self, sql, value=None):
        '''
        :summary: 向数据表插入一条记录
        :param sql: 要插入的sql格式
        :param value: 要插入的记录数据tuple/list
        :return: insertId受影响的行上
        '''
        if value:
            self._cursor.execute(sql, value)
        else:
            self._cursor.execute(sql)
        self._conn.commit()
        return self.__get_insertId()

    def insert_many(self, sql, values=None):
        '''
        :summary: 向数据表插入多条记录
        :param sql: 插入的sql格式
        :param values: 要插入的记录数据tuple(tuple)/list[list]
        :return: count 受影响的行数
        '''
        if values:
            count = self._cursor.executemany(sql, values)
        else:
            count = self._cursor.executemany(sql)
        self._conn.commit()
        return count

    def __get_insertId(self):
        '''
        获取当前连接最后一次插入操作生成的id,如果没有则为0
        :return:
        '''
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        '''
        :summary: 执行sql
        :param sql:
        :param param:
        :return:
        '''
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        '''
        :summary: 更新数据表记录
        :param sql: sql格式及条件，使用（%s,%s）
        :param param: 要更新的值 tuple/list
        :return: count受影响的行数
        '''
        if param is None:
            result = self.__query(sql)
        else:
            result = self.__query(sql, param)
        self._conn.commit()
        return result


    def delete(self, sql, param=None):
        '''
        :summary: 删除数据表记录
        :param sql: sql格式及条件，使用(%s,%s)
        :param param: 要删除的条件，值(tuple/list)
        :return: count受影响的行数
        '''
        if param is None:
            result = self.__query(sql)
        else:
            result = self.__query(sql, param)
        self._conn.commit()
        return result

    def begin(self):
        '''开启事务'''
        self._conn.autocommit(0)

    def end(self, option='commit'):
        '''事务结束'''
        if option == 'commit':
            self._conn.commit()  # 提交
        else:
            self._conn.rollback()  # 回滚

    def dispose(self, isEnd=1):
        '''释放连接池资源'''
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
