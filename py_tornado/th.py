#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016/11/25 17:30
# @Author  : xycfree
# @Link    : http://example.org
# @Version : $

import os
import threading
from main import MainHandler
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
result = {}


class Th(threading.Thread):
    def __init__(self, a, b, c):
        super(Th, self).__init__()
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)

        self.wx = aa(self.a, self.b, self.c)
        self.zh = bb(self.a, self.b, self.c)
        self.news = cc(self.a, self.b, self.c)
        self.tieba = dd(self.a, self.b, self.c)

    def run(self):
        result[self.wx] = self.wx
        result[self.zh] = self.zh
        result[self.news] = self.news
        result[self.tieba] = self.tieba


def aa(aa, b, c):
    return aa + b + c


def bb(aa, b, c):
    return (aa + b + c) * 2


def cc(aa, b, c):
    return (aa + b + c) * 4


def dd(aa, b, c):
    return (aa + b + c) * 8


if __name__ == '__main__':
    print aa(11, 33, 33)
    t = Th(3, 5, 2)
    t.start()
    print(result)
