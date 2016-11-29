#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/29 11:26
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import logging
import ctypes
#from logging.handlers import RotatingFileHandler
from datetime import datetime
log_folder = '../logs'
log_file = 'info_' + datetime.now().strftime('%Y-%m-%d') + '.log'
path = os.path.join(log_folder,log_file)

# Log_debug = logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S',
#                 filename= os.path.join(log_folder,'info.log'),
#                 filemode='a+')

#默认情况下，logging将日志打印到屏幕，日志级别为WARNING；
#日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，当然也可以自己定义日志级别。
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#

#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
'''
Rthandler = RotatingFileHandler('myapp.log', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
'''


FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

class Logger:
    def __init__(self, path=path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message, color=FOREGROUND_YELLOW):
        set_color(color)
        self.logger.warn(message)
        set_color(FOREGROUND_WHITE)

    def error(self, message, color=FOREGROUND_RED):
        set_color(color)
        self.logger.error(message)
        set_color(FOREGROUND_WHITE)

    def cri(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logyyx = Logger(path, logging.WARNING, logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')